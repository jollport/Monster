#!/usr/bin/env python3
"""
laptop-info.py - Identifies laptop system information
Usage: python laptop-info.py
"""

import platform
import subprocess
import sys

def get_system_info():
    """Collect and display system information"""
    
    print("=" * 50)
    print("LAPTOP SYSTEM INFORMATION")
    print("=" * 50)
    
    # Basic system info
    print(f"\n📋 BASIC SYSTEM:")
    print(f"  System: {platform.system()}")
    print(f"  Node Name: {platform.node()}")
    print(f"  Release: {platform.release()}")
    print(f"  Version: {platform.version()}")
    print(f"  Machine: {platform.machine()}")
    print(f"  Processor: {platform.processor()}")
    
    # Platform-specific info
    if platform.system() == "Windows":
        get_windows_info()
    elif platform.system() == "Linux":
        get_linux_info()
    elif platform.system() == "Darwin":
        get_macos_info()
    
    # Python info
    print(f"\n🐍 PYTHON ENVIRONMENT:")
    print(f"  Python Version: {platform.python_version()}")
    print(f"  Python Compiler: {platform.python_compiler()}")
    print(f"  Python Implementation: {platform.python_implementation()}")

def get_windows_info():
    """Get Windows-specific information"""
    try:
        import wmi
        c = wmi.WMI()
        
        print(f"\n🖥️ WINDOWS SPECIFIC:")
        
        # Computer system info
        for computer in c.Win32_ComputerSystem():
            print(f"  Manufacturer: {computer.Manufacturer}")
            print(f"  Model: {computer.Model}")
            print(f"  System Type: {computer.SystemType}")
            
        # OS info
        for os_info in c.Win32_OperatingSystem():
            print(f"  OS Name: {os_info.Caption}")
            print(f"  OS Architecture: {os_info.OSArchitecture}")
            
        # CPU info
        for cpu in c.Win32_Processor():
            print(f"  CPU: {cpu.Name}")
            print(f"  Cores: {cpu.NumberOfCores}")
            print(f"  Logical Processors: {cpu.NumberOfLogicalProcessors}")
            
        # RAM info
        for mem in c.Win32_PhysicalMemory():
            total_memory = sum([int(m.Capacity) for m in c.Win32_PhysicalMemory()])
            print(f"  Total RAM: {total_memory // (1024**3)} GB")
            break
            
    except ImportError:
        print("\n⚠️ Install 'wmi' package for detailed Windows info:")
        print("  pip install wmi")

def get_linux_info():
    """Get Linux-specific information"""
    try:
        print(f"\n🐧 LINUX SPECIFIC:")
        
        # Distribution info
        result = subprocess.run(['lsb_release', '-a'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  Distribution Info:\n{result.stdout}")
        
        # Memory info
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                if 'MemTotal' in line:
                    mem = int(line.split()[1]) // 1024
                    print(f"  Total RAM: {mem} MB")
                    break
        
        # CPU info
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if 'model name' in line:
                    print(f"  CPU: {line.split(':')[1].strip()}")
                    break
        
        # Check battery info (for laptops)
        try:
            result = subprocess.run(['upower', '-i', '/org/freedesktop/UPower/devices/battery_BAT0'], 
                                  capture_output=True, text=True)
            if 'model' in result.stdout:
                for line in result.stdout.split('\n'):
                    if 'model' in line or 'vendor' in line:
                        print(f"  {line.strip()}")
        except:
            pass
            
    except FileNotFoundError:
        print("  (Some Linux commands not available)")

def get_macos_info():
    """Get macOS-specific information"""
    try:
        print(f"\n🍎 macOS SPECIFIC:")
        
        # Hardware model
        result = subprocess.run(['sysctl', '-n', 'hw.model'], 
                              capture_output=True, text=True)
        if result.stdout:
            print(f"  Model: {result.stdout.strip()}")
        
        # CPU info
        result = subprocess.run(['sysctl', '-n', 'machdep.cpu.brand_string'], 
                              capture_output=True, text=True)
        if result.stdout:
            print(f"  CPU: {result.stdout.strip()}")
        
        # Memory info
        result = subprocess.run(['sysctl', '-n', 'hw.memsize'], 
                              capture_output=True, text=True)
        if result.stdout:
            mem_gb = int(result.stdout.strip()) // (1024**3)
            print(f"  Total RAM: {mem_gb} GB")
        
        # macOS version
        result = subprocess.run(['sw_vers', '-productVersion'], 
                              capture_output=True, text=True)
        if result.stdout:
            print(f"  macOS Version: {result.stdout.strip()}")
            
    except FileNotFoundError:
        print("  (macOS commands not available)")

if __name__ == "__main__":
    get_system_info()
