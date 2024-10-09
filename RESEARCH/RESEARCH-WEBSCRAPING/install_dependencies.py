import subprocess
import sys


def install_package(package_name):
    """
    Install a Python package using pip.
    
    :param package_name: The name of the package to install.
    """
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"'{package_name}' installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing {package_name}: {e}")


def main():
    """
    Main function to install Selenium, BeautifulSoup, and webdriver-manager.
    """
    # List of packages to install
    packages = ['selenium', 'beautifulsoup4', 'webdriver-manager']

    # Install each package
    for package in packages:
        install_package(package)


if __name__ == '__main__':
    main()

