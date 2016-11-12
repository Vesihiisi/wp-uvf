#WP-UVF

A script to assist in importing biographies from the Creative Commons-licensed encyclopedia [Uppslagsverket Finland](http://uppslagsverket.fi/) to Swedish Wikipedia, using the Beautiful Soup library.

It downloads an article and performs some basic formatting tasks, like adding birth/death year categories and templates. The output [looks like this](https://gist.github.com/Vesihiisi/ca1cc6f058b4870dd5edba2edca25775).

## Usage

Pass the article url as an argument.

```
python3 uvf.py http://www.uppslagsverket.fi/sv/sok/view-103684-PeltolaHeikki
```
