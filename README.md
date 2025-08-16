# quaint
quaint (*qu*ick *ai* li*nt*) takes an input document (plain text or pdf) and uses an llm to lint and format the text.

it turns this noisy OCR scan:
```
48

49
50
50a
ASL

51
AS2
52

REVISED 8/19/2017
-- 33-36.

David dives headfirst onto the small bed. He grabs the
pillow and hugs it tightly. A single tear runs down
his cheek.
DISSOLVE TO:
OMIT 43
OMIT 49
OMIT 50
OMIT SOA
EXT. HOTEL - MORNING ASL
David and Steve walk out of the hotel onto the sunny
street. David looks tired.
STEVE

It's not that big a city, David.

I'll bet there's an arcade at

every corner.
The boys look up the block then turn and look down
the other way.

STEVE
Let's try the next street.
cur To:

OMIT 51
OMIT AS2
```
into this properly formatted screenplay:
```
David dives headfirst onto the small bed. He grabs the pillow and hugs it tightly. A single tear runs down his cheek.

DISSOLVE TO:

EXT. HOTEL - MORNING

David and Steve walk out of the hotel onto the sunny street. David looks tired.

STEVE
It's not that big a city, David. I bet there's an arcade at every corner.

The boys look up the block then turn and look down the other way.

STEVE
Let's try the next street.

CUT TO:
```
