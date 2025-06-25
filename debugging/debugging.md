# DOM Debugging Guide for Catalog Scraper

## Motivation 
Websites often change their structure, class names, or nesting patterns. This guide helps identify and fix issues that arise when the Document Object Model (DOM) changes, particularly when elements can no longer be found using existing selectors.

It provides a quick reference of what lines in the code expect from the page structure, and how to inspect and correct those if things break.


## How to use
1. Look at error message or log.
2. Find corresponding code snippet below and match it actual code.
3. Open the corresponding page in browser (url in parameter) 
4. Right-click page and click Inspect Element and find where code snippet is failing. ([DevTools Guide](https://developer.chrome.com/docs/devtools/open))
5. Update the selector in code based on this. 

## Example

if the class tag has changed, update it.
```
    siteMap = soup.find('div', class_='oldValue')
    siteMap = soup.find('div', class_='newValue')
```
or perhaps if the element and class change update both.
```
    siteMap = soup.find('div', class_='oldValue')
    siteMap = soup.find('a', class_='newValue')
```

## Common selectors and reference screen shots (6/25/25)

```
def scrapeCatalogFrontPage(URL):
    ...
    siteMap = soup.find('div', class_='sitemap')
    allMajors = siteMap.find_all('a', class_='sitemaplink')
    ...
```

![sitemap](/debugging/images/scrapeCatalogFrontPage(sitemap).png)
![sitemapLink](/debugging/images/scrapeCatalogFrontPage(sitemaplink).png)  


```
def scrapeSubject(URL_subject):
    ...
    courseBlock = soup.find('div', class_="sc_sccoursedescs")
    allCourses = courseBlock.find_all('div', class_='courseblock')
    ...
```

![sc_sccoursedescs](/debugging/images/scrapeSubject(sc_sccoursedescs).png)
![courseblock](/debugging/images/scrapeSubject(courseblock).png)