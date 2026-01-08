#!/usr/bin/env python3
"""
Space Entropy Generator - Startup Script
Starts both backend (Docker) and frontend (npm) services
"""

import subprocess
import sys
import time
import signal
import os
from pathlib import Path

# Color codes for terminal output
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
RESET = '\033[0m'

# Global process handlers
processes = []

def print_header():
    """Print startup banner"""
    print(f"\n{BOLD}{BLUE}{'='*60}{RESET}")
    print(f"{BOLD}{GREEN}🌌 Space Image Based Entropy Generator{RESET}")
    print(f"{BOLD}{BLUE}   True Randomness as a Service{RESET}")
    print(f"{BOLD}{BLUE}{'='*60}{RESET}\n")

def print_status(message, status="info"):
    """Print colored status message"""
    colors = {
        "info": BLUE,
        "success": GREEN,
        "warning": YELLOW,
        "error": RED
    }
    color = colors.get(status, BLUE)
    symbols = {
        "info": "ℹ",
        "success": "✓",
        "warning": "⚠",
        "error": "✗"
    }
    symbol = symbols.get(status, "•")
    print(f"{color}{symbol} {message}{RESET}")

def cleanup(signum=None, frame=None):
    """Cleanup function to stop all processes"""
    print(f"\n{YELLOW}🛑 Shutting down services...{RESET}")
    
    # Stop frontend
    for proc in processes:
        try:
            proc.terminate()
            proc.wait(timeout=5)
            print_status("Frontend stopped", "success")
        except:
            try:
                proc.kill()
            except:
                pass
    
    # Stop Docker containers
    print_status("Stopping Docker containers...", "info")
    subprocess.run(["docker-compose", "down"], capture_output=True)
    print_status("Docker containers stopped", "success")
    
    print(f"\n{GREEN}✓ All services stopped successfully{RESET}\n")
    sys.exit(0)

def check_docker():
    """Check if Docker is available"""
    try:
        subprocess.run(["docker", "--version"], capture_output=True, check=True)
        return True
    except:
        return False

def check_npm():
    """Check if npm is available"""
    try:
        subprocess.run(["npm", "--version"], capture_output=True, check=True)
        return True
    except:
        return False

def start_backend():
    """Start backend services with Docker Compose"""
    print_status("Starting backend services (Redis + FastAPI)...", "info")
    
    try:
        # Build and start containers
        subprocess.run(["docker-compose", "up", "-d", "--build"], check=True)
        print_status("Backend containers started", "success")
        
        # Wait for backend to be healthy
        print_status("Waiting for backend to be healthy...", "info")
        max_retries = 30
        for i in range(max_retries):
            try:
                result = subprocess.run(
                    ["curl", "-s", "http://localhost:8000/api/v1/health"],
                    capture_output=True,
                    timeout=2
                )
                if result.returncode == 0:
                    print_status("Backend is healthy", "success")
                    return True
            except:
                pass
            time.sleep(2)
            if (i + 1) % 5 == 0:
                print_status(f"Still waiting... ({i + 1}/{max_retries})", "warning")
        
        print_status("Backend health check timeout (but may still be starting)", "warning")
        return True
        
    except subprocess.CalledProcessError as e:
        print_status(f"Failed to start backend: {e}", "error")
        return False

def start_frontend():
    """Start frontend development server"""
    print_status("Starting frontend (React + Vite)...", "info")
    
    # Get frontend directory
    frontend_dir = Path(__file__).parent / "website" / "solar-entropy-api-main" / "solar-entropy-api-main"
    
    if not frontend_dir.exists():
        print_status(f"Frontend directory not found: {frontend_dir}", "error")
        return None
    
    try:
        # Check if node_modules exists, if not run npm install
        node_modules = frontend_dir / "node_modules"
        if not node_modules.exists():
            print_status("Installing frontend dependencies (this may take a minute)...", "info")
            subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
            print_status("Dependencies installed", "success")
        
        # Start dev server
        print_status("Launching Vite dev server...", "info")
        proc = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Wait for Vite to start
        time.sleep(3)
        
        if proc.poll() is None:
            print_status("Frontend server started", "success")
            return proc
        else:
            print_status("Frontend failed to start", "error")
            return None
            
    except Exception as e:
        print_status(f"Failed to start frontend: {e}", "error")
        return None

def print_summary():
    """Print summary of running services"""
    print(f"\n{BOLD}{GREEN}{'='*60}{RESET}")
    print(f"{BOLD}{GREEN}🚀 All services are running!{RESET}")
    print(f"{BOLD}{GREEN}{'='*60}{RESET}\n")
    
    print(f"{BOLD}Service URLs:{RESET}")
    print(f"  {BLUE}Frontend (Web UI):{RESET}      http://localhost:8080")
    print(f"  {BLUE}Backend API:{RESET}            http://localhost:8000")
    print(f"  {BLUE}API Documentation:{RESET}     http://localhost:8000/docs")
    print(f"  {BLUE}Health Check:{RESET}          http://localhost:8000/api/v1/health")
    
    print(f"\n{BOLD}Quick Commands:{RESET}")
    print(f"  {YELLOW}Get random bytes:{RESET}     curl http://localhost:8000/api/v1/random/256")
    print(f"  {YELLOW}Check pool stats:{RESET}     curl http://localhost:8000/api/v1/stats")
    print(f"  {YELLOW}View backend logs:{RESET}    docker logs -f space_entropy_app")
    
    print(f"\n{BOLD}{RED}Press CTRL+C to stop all services{RESET}\n")

def main():
    """Main function"""
    # Setup signal handlers
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)
    
    # Print header
    print_header()
    
    # Check prerequisites
    print_status("Checking prerequisites...", "info")
    
    if not check_docker():
        print_status("Docker not found. Please install Docker first.", "error")
        sys.exit(1)
    
    if not check_npm():
        print_status("npm not found. Please install Node.js and npm first.", "error")
        sys.exit(1)
    
    print_status("All prerequisites satisfied", "success")
    
    # Start backend
    print(f"\n{BOLD}Step 1: Starting Backend{RESET}")
    if not start_backend():
        print_status("Failed to start backend. Exiting.", "error")
        sys.exit(1)
    
    # Start frontend
    print(f"\n{BOLD}Step 2: Starting Frontend{RESET}")
    frontend_proc = start_frontend()
    if frontend_proc is None:
        print_status("Failed to start frontend. Stopping backend...", "error")
        subprocess.run(["docker-compose", "down"], capture_output=True)
        sys.exit(1)
    
    processes.append(frontend_proc)
    
    # Print summary
    time.sleep(2)
    print_summary()
    
    # Keep running and monitor processes
    try:
        while True:
            # Check if frontend process is still running
            if frontend_proc.poll() is not None:
                print_status("Frontend process stopped unexpectedly", "error")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        cleanup()

if __name__ == "__main__":
    main()
