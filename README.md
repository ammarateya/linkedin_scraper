# LinkedIn Comment Scraper

This is a Python script that extracts comments from a LinkedIn post and saves them to a CSV file.

## Installation

### Clone the Repository

```bash
git clone https://github.com/<YOUR_USERNAME>/linkedin-comment-scraper.git
cd linkedin-comment-scraper
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Set Up Environment Variables

Create a `.env` file in the root directory of the project and add the following variables:

```
EMAIL=<Your LinkedIn Email>
PASSWORD=<Your LinkedIn Password>
```

### Download ChromeDriver

Download the appropriate version of ChromeDriver based on your Chrome browser version, or download the chrome for testing, and its accompanying webdriver, like I did, because I don't use Chrome, I use Arc. (go arc yay) After downloading, extract the `chromedriver` executable and move it to the project directory.

## Usage

Run the script with the following command:

```bash
python script.py <linkedin_post_url>
```

Replace `<linkedin_post_url>` with the URL of the LinkedIn post from which you want to extract comments.

## Example

```bash
python script.py https://www.linkedin.com/posts/dr-miquel-noguer-i-alonso-7242345_james-harris-simons-1938-may-10-2024-ugcPost-7194739148195278848-sffT/
```

## Change it up
if you want to change it up, and use this for other linkedin stuff, make sure you pay close attention to the tags, because selenium is kinda picky about what you put as parameters. check out the documentation here, it's pretty easy to read: https://www.selenium.dev/documentation/overview/

## License

This project is not licensed :)
