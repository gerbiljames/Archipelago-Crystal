# Guidelines for PRs that add new Phone Traps

## Technical Guidelines
- Every phone call can only be a max of 1024 bytes (1kib). This will be assured via unit test. Just be aware there is a limit.
- A line is max 17 characters long. This will be assured via unit test. Just be aware of the limit when writing it.
- When using RIVAL or PLAYER variables, assume they are the max of 6 characters.
- We cannot add new callers. [All available callers can be found here.](https://github.com/gerbiljames/Archipelago-Crystal/blob/2499f228aefadeb49b627f0e90a2f0a338277d26/worlds/pokemon_crystal/phone_data.py#L39-L49) Use None / Withheld / Out of Area / at your discretion
- The "commands" you can use (variables, etc.) [can be found here with explanations.](https://github.com/gerbiljames/Archipelago-Crystal/blob/2499f228aefadeb49b627f0e90a2f0a338277d26/worlds/pokemon_crystal/phone_data.py#L51-L60)
- Only submit ONE Phone Trap per Pull Request

## Content Guidelines
- Look at the original 16 phone traps. We want the kind of humor to be adjacent to that.
- The humor has to be funny without context. Except Pokémon humor - you may assume everyone knows all Pokémon lore.
- The phone traps do not have to be Pokémon-related.
- They have to be SFW (appropriate for 17 years old).
- They *can* contain references to copyrighted content. They *cannot* contain copyrighted content.

# Submission Considerations
- A submission has to be approved by at least 5 users by giving a "Thumbs Up" reaction on the PR
- Two of these approvals need to be @gerbiljames and @palex00
- This requirement may change as we learn with the system
