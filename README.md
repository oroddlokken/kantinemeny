# Lunch menu scraper for Toma cafeterias

Public preview and examples:
- [https://lunsj.rkrkn.no/](https://lunsj.rkrkn.no/)
- [https://lunsj.rkrkn.no/api/](https://lunsj.rkrkn.no/api/)
- [https://lunsj.rkrkn.no/NordreNostekai1](https://lunsj.rkrkn.no/NordreNostekai1)
- [https://lunsj.rkrkn.no/api/NordreNostekai1](https://lunsj.rkrkn.no/api/NordreNostekai1)

#### Special content
To show special special content for special visitors, add the following files:
- special_visitors.json in the root folder with the IP adresses of your special visitors, like so:  
```
{
    "1.2.3.4": "some_comment",
    "5.6.7.8": "another_comment"
}
```
- special_content.html in the templates folder with the extra content you want to show your special visitors
