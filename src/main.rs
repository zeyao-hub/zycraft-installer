mod manifest;

use std::process::Command;
use std::path::Path;
use reqwest;
use indicatif::{ProgressBar, ProgressStyle};
use tokio;
use std::fs::File;
use std::io::Write;
use futures_util::StreamExt;
use is_elevated::is_elevated;
use std::process;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // 检查是否具有管理员权限
    if !is_elevated() {
        println!("需要管理员权限来安装 Python。正在请求管理员权限...");

        // 获取当前可执行文件路径
        let current_exe = std::env::current_exe()?;

        // 以管理员权限重新启动程序
        let mut command = std::process::Command::new("powershell");
        command.args(&[
            "Start-Process",
            &current_exe.to_string_lossy(),
            "-Verb",
            "RunAs"
        ]);

        match command.spawn() {
            Ok(_) => {
                println!("已请求管理员权限，请在弹出的 UAC 窗口中确认。");
                process::exit(0);
            }
            Err(e) => {
                println!("无法获取管理员权限: {}", e);
                process::exit(1);
            }
        }
    }

    println!("开始检测 Python 安装状态...");

    let initial_check = check_python_version();
    if let Some(version) = initial_check {
        println!("系统已安装 Python {}", version);
        wait_for_exit();
        return Ok(());
    }

    println!("未检测到 Python，开始下载安装 Python 3.11.9...");
    install_python().await?;

    // 安装后等待几秒钟让系统刷新环境变量
    println!("等待系统更新环境变量...");
    std::thread::sleep(std::time::Duration::from_secs(5));

    // 验证安装结果
    match verify_installation() {
        Ok(()) => {
            println!("√ Python 安装验证成功！");
            refresh_environment_variables()?;
        }
        Err(e) => println!("× Python 安装验证失败：{}", e),
    }

    wait_for_exit();
    Ok(())
}

fn wait_for_exit() {
    println!("\n按回车键下一步...");
    let mut input = String::new();
    std::io::stdin().read_line(&mut input).unwrap();
}

fn refresh_environment_variables() -> Result<(), Box<dyn std::error::Error>> {
    // 刷新环境变量
    let refresh_cmd = r#"
        $Process = New-Object -TypeName System.Diagnostics.Process
        $Process.StartInfo.FileName = "powershell.exe"
        $Process.StartInfo.Arguments = '-NoProfile -NonInteractive -Command "$env:Path = [System.Environment]::GetEnvironmentVariable(\"Path\",\"Machine\") + \";\" + [System.Environment]::GetEnvironmentVariable(\"Path\",\"User\")"'
        $Process.StartInfo.UseShellExecute = $false
        $Process.Start()
        $Process.WaitForExit()
    "#;

    Command::new("powershell")
        .args(&["-Command", refresh_cmd])
        .output()?;

    Ok(())
}

fn check_python_version() -> Option<String> {
    let output = Command::new("python")
        .args(&["--version"])
        .output()
        .ok()?;

    if output.status.success() {
        let version = String::from_utf8_lossy(&output.stdout);
        Some(version.trim().to_string())
    } else {
        None
    }
}

async fn install_python() -> Result<(), Box<dyn std::error::Error>> {
    let python_url = "https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe";
    let installer_path = "python_installer.exe";

    // 下载安装程序
    download_file(python_url, installer_path).await?;

    println!("下载完成，开始安装...");

    // 执行安装
    let install_result = Command::new(installer_path)
        .args(&[
            "/quiet",
            "InstallAllUsers=1",
            "PrependPath=1",
            "Include_test=0",
            "Include_pip=1"
        ])
        .output()?;

    if install_result.status.success() {
        println!("Python 3.11.9 安装程序执行完成！");
        // 清理安装文件
        std::fs::remove_file(installer_path)?;
    } else {
        println!("安装失败，请检查权限或手动安装。");
        println!("错误信息: {:?}", String::from_utf8_lossy(&install_result.stderr));
        return Err("安装失败".into());
    }

    Ok(())
}

async fn download_file(url: &str, path: &str) -> Result<(), Box<dyn std::error::Error>> {
    let client = reqwest::Client::new();
    let res = client.get(url).send().await?;
    let total_size = res.content_length().unwrap_or(0);

    // 创建进度条
    let pb = ProgressBar::new(total_size);
    pb.set_style(ProgressStyle::default_bar()
        .template("{spinner:.green} [{elapsed_precise}] [{bar:50.cyan/blue}] {bytes}/{total_bytes} ({eta})")
        .unwrap()
        .progress_chars("#>-"));

    // 打开文件准备写入
    let mut file = File::create(path)?;
    let mut downloaded: u64 = 0;
    let mut stream = res.bytes_stream();

    // 下载文件并更新进度条
    while let Some(chunk) = stream.next().await {
        let chunk = chunk?;
        file.write_all(&chunk)?;
        downloaded = std::cmp::min(downloaded + (chunk.len() as u64), total_size);
        pb.set_position(downloaded);
    }

    pb.finish_with_message("下载完成");
    Ok(())
}

fn verify_installation() -> Result<(), Box<dyn std::error::Error>> {
    // 检查 Python 版本
    let version_check = Command::new("python")
        .args(&["--version"])
        .output()?;

    if !version_check.status.success() {
        return Err("无法执行 python --version".into());
    }

    let version = String::from_utf8_lossy(&version_check.stdout);
    println!("检测到安装的 Python 版本: {}", version.trim());

    // 检查 pip 是否可用
    let pip_check = Command::new("pip")
        .args(&["--version"])
        .output()?;

    if !pip_check.status.success() {
        return Err("pip 安装失败".into());
    }

    println!("pip 安装状态: {}", String::from_utf8_lossy(&pip_check.stdout).trim());

    // 测试 Python 是否能正常运行
    let python_test = Command::new("python")
        .args(&["-c", "print('Hello from Python!')"])
        .output()?;

    if !python_test.status.success() {
        return Err("Python 执行测试失败".into());
    }

    let test_output = String::from_utf8_lossy(&python_test.stdout);
    if test_output.trim() != "Hello from Python!" {
        return Err("Python 执行结果异常".into());
    }

    // 检查环境变量
    if let Ok(path) = std::env::var("PATH") {
        if !path.to_lowercase().contains("python") {
            println!("警告: Python 可能未正确添加到 PATH 环境变量");
        }
    }

    Ok(())
}