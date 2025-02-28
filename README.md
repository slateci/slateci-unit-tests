# [slateci.io](https://slateci.io/) Selenium Web App Unit Test

[![License: Unlicense](https://img.shields.io/badge/license-Unlicense-blue.svg)](http://unlicense.org/)

[Selenium](https://www.selenium.dev/documentation/en/) is a framework for automating web applications tests. It runs on OS's such as Windows, Mac OS, Linux and Solaris. It's supported browsers include Chrome, FireFox, Edge, Internet Explorer, Safari and Opera. The Selenium client API supports Java, Python, C#, Ruby, JavaScript and Kotlin.

## Test Suite Structure

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

## Running the Test Suite

### GitHub Actions

In the [slateci.io repo](https://github.com/slateci/slateci.github.io), the GitHub Actions testing procedure is set up in [selenium-tests.yml](https://github.com/slateci/slateci.github.io/blob/master/.github/workflows/selenium-tests.yml). The test is set up tp run on `push` or `pull request` to the `master` branch of the [slateci.io repository](https://github.com/slateci/slateci.github.io). Below is the list of the test setup and running procedure:
1. Setup Python 3.8 
2. Install Selenium Python bindings
3. Install Chrome web driver. After installation, the path to the web driver will be at `/home/runner/work/slateci.github.io/slateci.github.io/chromedriver`
4. Download Selenium test. The test program in this repository will be downloaded to the GitHub Actions VM in the [slateci.io repo](https://github.com/slateci/slateci.github.io)
5. Run Selenium Tests
6. Post Slack to `#website` if the test failed.

### Docker

#### Testing on Production

Run the test suite on the production website:

```shell
[your@localmachine ~]$ docker run -it -v $PWD:/opt/project joyzoursky/python-chromedriver:3.9-selenium python /opt/project/main.py
INFO     URL under test: https://slateci.io/
...
...
```

* Use the `$PWD:/opt/project` volume to mount files from the host to the container.
* The Python installation in the image may be used as a remote interpreter in IDEs such as [VSCode](https://devblogs.microsoft.com/python/remote-python-development-in-visual-studio-code/) and [IntelliJ](https://www.jetbrains.com/help/idea/configuring-remote-python-sdks.html).

#### Testing on Local Build

Run the test suite on a local containerized build of the website:

```shell
[your@localmachine ~]$ docker run -it -v $PWD:/opt/project --network="host" joyzoursky/python-chromedriver:3.9-selenium python /opt/project/main.py http://localhost:4000
INFO     URL under test: http://localhost:4000
...
...
```

* Use the `$PWD:/opt/project` volume to mount files from the host to the container.
* The Python installation in the image may be used as a remote interpreter in IDEs such as [VSCode](https://devblogs.microsoft.com/python/remote-python-development-in-visual-studio-code/) and [IntelliJ](https://www.jetbrains.com/help/idea/configuring-remote-python-sdks.html).
* Refer to [slateci/slateci.github.io](https://github.com/slateci/slateci.github.io) for additional information on running the website locally.

### Local Machine

#### Minimum Requirements

* Operating Systems: Linux or macOS
* Browsers: Chrome or Firefox
* Python 3
* Selenium library for Python
  ```shell
  $ pip install selenium
  ```
* Reference: [Selenium documentation](https://www.selenium.dev/documentation/en/)

#### Install Web Driver (Google Chrome)

* Referenced [Documentation](https://selenium-python.readthedocs.io/installation.html)
* Download and unzip the web driver
* This instruction assumes the download path is at `/opt/WebDriver/bin`. The users can specify other download path as needed.

#### Chrome WebDriver Download

* Selenium requires a web driver of corresponding version to interface with the installed Chrome. Check the Chrome version before installation
* For example, if the Chrome version is `84.0.4147.105`, then `ChromeDriver 84.0.4147.30` should be downloaded from [WebDriver for Chrome](https://sites.google.com/a/chromium.org/chromedriver/downloads)

#### Add Download Directory to PATH

```shell
$ export PATH=$PATH:/opt/WebDriver/bin >> ~/.profile
```

* If the above command does not work in macOS, add line `export PATH=$PATH:/opt/WebDriver/bin` to file `~/.bash_profile`

#### Bypass the Notarization Requirement on macOS

* macOS notarization requirement can prevent the web driver from running
* Navigate to the folder containing the web driver.
* For `chromedriver` run the following command:
  ```shell
  $ xattr -r -d com.apple.quarantine chromedriver 
  ```
#### Run Test

* `git clone` this repo to local machine
* In `main.py` -> `setUp(self)`, change the `path` variable to the absolute path of the Chrome web driver in the local machine
* In `main.py` -> `setUp(self)`, set `options.headless = True` to run test in the background, or set `options.headless = False` to run test on a open browser session
* In the terminal, `cd` into the test program folder, run:
  ```bash
  $ python main.py
  ```
