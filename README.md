## What it does

Add one Logic Test slot alongside one or more games-under-test. During generation it generates the under-test slots together as one nested multiworld, reads their overall (cross-game) sphere structure, and rebuilds itself as a linear chain of gated spheres matching it:

- Every under-test item is pulled out and locked into a Logic Test sphere location.
- Each under-test location instead receives a `KEY_i` mcguffin.
- Sphere `i` only opens once the slot has collected every `KEY_i`, releasing that sphere's original items.

Play is forced into lock-step with the intended spheres without contamination of items from other spheres. This can help reveal two kind of logic gaps:
- Negative logic gaps: the apworld logic requires less items than are actually neccessary. As such, you will not be able to get all ``KEY_i`` mcguffins for the current sphere
- Positive logic gaps: the apworld logic requires more items than are actually neccessary. This will show by you being able to obtain ``KEY_i`` items for spheres above the current one

## Setup

Add one Logic Test slot (via YAML) plus one or more games-under-test. Slot order does not matter, since each under-test game's RNG is reproduced from its slot number, so YAMLs can be in any order.

## Limits

- Up to 512 spheres
- Up to 100,000 locations (items in the multiworld across all under-test games)

## Assets

- `logic_test.apworld`: the world, drop into your Archipelago `custom_worlds` (or `worlds`) directory
- `Logic Test.yaml`: a template options YAML

Requires Archipelago 0.6.7 or newer.

## AI Disclosure
Everything of this apworld, including the text above, was made by James using Claude. The idea was by palex00, a human. This apworld was tested to work by palex00. 
