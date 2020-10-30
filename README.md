# [slateci.io](https://slateci.io/) Selenium Web App Unit Test

[Selenium](https://www.selenium.dev/documentation/en/) is a framework for automating web applications tests. It runs on OS's such as Windows, Mac OS, Linux and Solaris. It's supported browsers include Chrome, FireFox, Edge, Internet Explorer, Safari and Opera. The Selenium client API supports Java, Python, C#, Ruby, JavaScript and Kotlin
## Minimum Requirement
- Operating Systems: Linux or macOS
- Browsers: Chrome or Firefox
- Python 3
- Selenium library for Python
    ```bash
    $ pip install selenium
    ```
- Reference: [Selenium documentation](https://www.selenium.dev/documentation/en/)


# Run Test in GitHub Actions
In the [slateci.io repo](https://github.com/slateci/slateci.github.io), the GitHub Actions testing procedure is set up in [selenium-tests.yml](https://github.com/slateci/slateci.github.io/blob/master/.github/workflows/selenium-tests.yml). The test is set up tp run on `push` or `pull request` to the `master` branch of the [slateci.io repository](https://github.com/slateci/slateci.github.io). Below is the list of the test setup and running procedure:
1. Setup Python 3.8 
2. Install Selenium Python bindings
3. Install Chrome web driver. After installation, the path to the web driver will be at `/home/runner/work/slateci.github.io/slateci.github.io/chromedriver`
4. Download Selenium test. The test program in this repository will be downloaded to the GitHub Actions VM in the [slateci.io repo](https://github.com/slateci/slateci.github.io)
5. Run Selenium Tests
6. Post Slack to `#website` if the test failed.

# Run Test in Local Machine
## 1) Install Web Driver (Google Chrome)
- Referenced [Documentation](https://selenium-python.readthedocs.io/installation.html)
- Download and unzip the web driver
- This instruction assumes the download path is at `/opt/WebDriver/bin`. The users can specify other download path as needed.

## 2) Chrome WebDriver Download
- Selenium requires a web driver of corresponding version to interface with the installed Chrome. Check the Chrome version before installation
- For example, if the Chrome version is `84.0.4147.105`, then `ChromeDriver 84.0.4147.30` should be downloaded from [WebDriver for Chrome](https://sites.google.com/a/chromium.org/chromedriver/downloads)

## 3) Add Download Directory to PATH
```bash
$ export PATH=$PATH:/opt/WebDriver/bin >> ~/.profile
```
- If the above command does not work in macOS, add line `export PATH=$PATH:/opt/WebDriver/bin` to file `~/.bash_profile`

## 4) Bypass the Notarization Requirement on macOS
- macOS notarization requirement can prevent the web driver from running
- Navigate to the folder containing the web driver.
- For `chromedriver` run the following command:
    ```bash
    xattr -r -d com.apple.quarantine chromedriver 
    ```
## 5) Run Test
- `git clone` this repo to local machine
- In `main.py` -> `setUp(self)`, change the `path` variable to the absolute path of the Chrome web driver in the local machine
- In `main.py` -> `setUp(self)`, set `options.headless = True` to run test in the background, or set `options.headless = False` to run test on a open browser session
- In the terminal, `cd` into the test program folder, run:
    ```bash
    python main.py
    ```
# Tests Structure 
    .
    ├── ...
    └── main.py                 
        └── WebPageBrowsing                 # tests to iterate through web pages
            ├── test_home_page              # check links on Home page
            ├── test_about_page             # check links on About page
            ├── test_tech_page              # check links on Technology page
            ├── test_docs_page              # check links on Docs page
            ├── test_blog_page              # check links on Blog page
            └── test_comm_page              # check links on Community page