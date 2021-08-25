# Naver News Comment Crawler

Project name is a `Naver News Comment Crawler` that allows `Anyone` to crawl `comments and titles from naver news portal`.

Used `scrapy` to boost up the speed and convenience.

## Installing

To install, follow these steps:

```
1. You have Chrome, right?
2. [Download](https://chromedriver.chromium.org/downloads) and add the correct version of `chromedriver` (you can check the version of yours in `preferences -> About Chrome`).
3. Install packages using `pip` / `conda` : you need `scrapy` and `selenium`
4. You're all set!
```

## Using <project_name>

To use crawler, follow these steps:

```
1. `scrapy crawl navernews -o {output_filename}
2. Write keyword to search news
3. Done!
```
The crawler now scrapes the title, date, and comments(including comments in comment)!

## Contributing to <project_name>
<!--- If your README is long or you have some specific process or steps you want contributors to follow, consider creating a separate CONTRIBUTING.md file--->
To contribute, follow these steps:

1. Fork this repository.
2. Create a branch: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create the pull request.

Alternatively see the GitHub documentation on [creating a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## Contact

If you want to contact me you can reach me at hoon2j@gmail.com
