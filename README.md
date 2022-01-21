# Card Converter

Take a pdf, where one side of a card is on each page. Front side and back side alternating:
page 1
```
----------
- card 1 -
- front  -
----------
```

page 2
```
----------
- card 1 -
- back   -
----------
```

page 3
```
----------
- card 2 -
- front  -
----------
```

page 4
```
----------
- card 2 -
- back   -
----------
```

etc...

Then, put them into a new pdf with DIN A4 pages, where the cards are located that if printed double-sided
the front and the back of each card is exact back-to-back. So if cut out, you have double-sided cards again.
There are eight cards on each page, four in a row with two rows.

page 1
```
----------  ----------
- card 1 -  - card 2 -
- front  -  - front  -
----------  ----------
```

page 2
```
----------  ----------
- card 2 -  - card 1 -
- back   -  - back   -
----------  ----------
```

## Usage Example
There are pdf files containing play card of Black Eye (Das Schwarze Auge - DSA) with gear and spells, etc.
On each page of the pdf there is one side of a card, front side and back side alternating. This script is used
to be able to print them to DIN A4, cut them out and for example to shrink-wrap them.
