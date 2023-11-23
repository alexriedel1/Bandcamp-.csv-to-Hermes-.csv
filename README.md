# Bandcamp CSV to Hermes CSV Converter

This script converts a Bandcamp exported shipping CSV to the format that is needed for Hermes CSV import.
This also includes splitting street name and number (tested for german addresses mostly) and converting the country name to the
Alpha 3 country code.

## Usage
```bash
pip install -r requirements.txt
```

```bash
bandcamp2hermes.py --file "path to your bandcamp csv file"
```

## Function

```python
10/16/23,max mustermann,muster@web.de,+49 01765553332,,Max Mustermann,Neue Bahnhofstraße 19a,,Berlin,,12345,Germany,DE,Band,"Product",,1,,23.23,0.00,6.00,29.23,EUR,Germany,,,,https://band.bandcamp.com/album/band,1234567891FFF,12318549643
```
to 

```python
Max;Mustermann;;Neue Bahnhofstraße;19a;12345;Berlin;;DEU;0049;1765553332;muster@web.de
```
