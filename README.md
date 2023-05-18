# Convert Freebase Entities and Relations to Wikidata

Google once implemented their own mapping guidance [google/freebase-wikidata-converter](https://github.com/google/freebase-wikidata-converter). However, it hasn't been updated for 8 years (it's 2023 at the time of writing). And the respository has been archived in 2022. This repository provides the best-effort mapping.

Since the mapping relies on real-time query, the results can always be up-to-date. The notebook [conversion.ipynb](./conversion.ipynb) provides detailed guidance on the mapping.

## Entities

We map the enities by looking up the [*Freebase ID*](https://www.wikidata.org/wiki/Property:P646) attribute of Wikidata entities,following the advice from [Freebase FAQ](https://www.wikidata.org/wiki/Help:FAQ/Freebase#How_can_I_map_my_Freebase_Mids_to_Wikidata_Qids?):

> How can I map my Freebase Mids to Wikidata Qids? <br>
> Wikidata has the property Freebase ID (P646) to add the Mid on a Wikidata item. Using WDQ, you can map single Mids to their Wikidata Item Qids, e.g. Query: string[646:"/m/02mjmr"]. You can also download Wikidata data and access Freebase ID (P646) in any of the other ways described here, i.e. from the dump, through the entity API, etc. See Wikidata:Data access for more details. 

Usage:

```python
from converter import EntityConverter

entity_converter = EntityConverter("https://query.wikidata.org/sparql")
entity_converter.get_wikidata_id("/m/0dgw9r")  # 'Q15978631'
entity_converter.get_freebase_id("Q42")  # '/m/0282x'
entity_converter.get_wikidata_id("/m/0dgw9r", limit=3)  # ['Q15978631', 'Q5']
```

4818298 entities from [Wikidata5m](https://deepgraphlearning.github.io/project/wikidata5m) are mapped and saved as a dictionary at [fid2qid.pkl](./fid2qid.pkl).

## Properties

The same [FAQ](https://www.wikidata.org/wiki/Help:FAQ/Freebase#How_can_I_map_a_Wikidata_property_to_a_Freebase_property?) page suggests to use [*equivalent property*](https://www.wikidata.org/wiki/Property:P1628) attribute to convert the properties. But it turns out that the Freebase link does not present in any property.

We get the latest property mapping by scraping [WikiProject Freebase/Mapping](https://www.wikidata.org/wiki/Wikidata:WikiProject_Freebase/Mapping) , which stores all existing property mappings.

Usage:

```python
from converter import PropertyConverter

property_converter = PropertyConverter("https://www.wikidata.org/wiki/Wikidata:WikiProject_Freebase/Mapping")
property_converter.get_wikidata_property("/organization/organization/child")  # 'P355'
property_converter.get_freebase_property("P355")  # '/organization/organization/child'
```
