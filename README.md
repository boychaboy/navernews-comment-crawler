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

## Using crawler

To use crawler, follow these steps:

```
1. `scrapy crawl navernews -o {output_filename}
2. Write keyword to search news
3. Done!
```
The crawler now scrapes the title, date, and comments(including comments in comment)!

## Contact

If you want to contact me you can reach me at hoon2j@gmail.com
