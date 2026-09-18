# Joseph Neyer Creations restoration

## Result

The original portfolio is reconstructed at `/joe/creations/`, with seven gallery screens, a page for the surviving porch photograph, and a short restoration note. It is intentionally unlinked from `/joe/` for initial sharing and review; the existing book and chapter anchors are unchanged.

Desktop artwork comes directly from the original SWF vectors: logo, outlined lettering, colors, layout, masks, and thumbnail compositions. Native HTML links and JavaScript replace Flash actions. Photographs are extracted from the movies, not screenshots. Small embedded thumbnails are downsampled; larger photographs are exported separately. The mobile layout uses the same images with touch-sized controls. Keyboard focus previews images; gallery arrows, click/tap, and full-photo links work without Flash. With JavaScript off, gallery links still open the photographs.

The implementation adds no runtime dependency or external service. `npm ci && npm run build` builds the full site with the existing Eleventy setup. `src/_data/joeCreations.json` contains original movie references, recovered button positions, destinations, and photographs. Checked-in derived assets make normal builds independent of the archive and extraction tools.

## Source record

Suzy's shared Google Drive folder: `1wc62GCRJvMNBQ6uFGahNquEVKaGNIOkI`, named `JoesWebsite`. Copied on 2026-09-17: **690 unique file paths, 789,123,352 bytes**. Local preservation root:

`/Users/uni/agents/gpt-sol-uni/REPOS/JOE_SUZY_ORIGINALS/`

`drive-manifest.json` records the Drive download URL and relative path. `download-receipts.json` records every successful download's byte size and SHA-256. `JoesWebsite/` retains original directory names and files. There are no failed receipts. These hashes describe the local copies; Drive did not supply independent reference hashes.

The preserved folder includes 404 JPEGs, 71 FLAs, 70 SWFs, 77 HTML files, two AVI files, five ZIPs, three DOCX files, the InDesign book source `joe/tmfdtsn6.29.indd`, and supporting design/office files. Originals remain outside the published site. Private correspondence, old business documents, and production files are not swept into the public assets.

## Fidelity and known gaps

- The home composition and the seven saved gallery compositions retain their original vector art. Brief Flash preload/morph animations are replaced by their settled state and direct image loading. SVG rendering/glow and JPEG compression can differ slightly from Flash.
- The original homepage points to `spporch.html` and `speery/speery1.swf`. Neither is in the shared folder. Its porch image survives as image object 43 in `indexfla.swf`; the restored porch page explains the gap and shows that photograph.
- `beeryfla.swf` and its nine child photographs survive, though the saved homepage does not link to that gallery. The archive footer provides access.
- The Elliot page has nine thumbnail positions but only five different linked photos: several original buttons reference `elliot5.swf`. That source behavior is retained. There are 70 thumbnail controls across the eight screens, not 70 distinct project photos.
- Some original button handlers contain stale unnumbered paths. Where the frame's named `onRollOver` handler gives a valid numbered destination, it takes precedence. The importer records the recovered references; it does not invent missing photos.
- The historical phone number and Email Me artwork remain visible on desktop, with their historical status explained on the restoration page. They do not initiate calls or email.
- The INDD book is preserved and its type verified. It has not been opened in InDesign or compared page-by-page with the existing EPUB/HTML book. No claim of edition equivalence is made.

## Extraction and reference inspection

Original site observed locally with [Ruffle](https://github.com/ruffle-rs/ruffle). Assets and ActionScript recovered with [JPEXS FFDec 26.3.0](https://github.com/jindrapetrik/jpexs-decompiler), following its [command-line documentation](https://github.com/jindrapetrik/jpexs-decompiler/wiki/Commandline-arguments).

Working extraction/reference directory on the mini:

`/Users/uni/.scratch/joe-restoration-tools/`

It contains the read-only original-site viewer, captured references, exported SWF XML/scripts/images/SVGs, `geometry.json`, and browser validation scripts. The reference viewer requires `base` to point to the original website directory; otherwise Flash's relative child-movie requests fail and the large photographs appear empty.

For the eight root movies, FFDec export settings were `-format frame:svg -select 3 -export frame,image,script,text`, followed by `-swf2xml`. For child movies: `-export image`. The home heading's settled sprite is `indexfla.swf` sprite 61 frame 49; the straight gallery heading is `atkinsfla.swf` sprite 61 frame 55. Export them with `-format sprite:svg -selectid 61 -select 61:49` (or `61:55`). Named thumbnail bounds were measured from the exported root SVG using Chromium's `getBoundingClientRect` at the original 2200×1000 stage size. XML connects instance names to button IDs, and ActionScript connects those IDs to images and page links.

`scripts/import-joe-creations.py` transforms that extracted data into the checked-in site assets. Run with `uv run --with pillow scripts/import-joe-creations.py /Users/uni/.scratch/joe-restoration-tools/extracted` to repeat the import in this workspace. The original Drive folder is never changed. The settled heading crops and logo crop are measured from the source art, not newly drawn.

## Preview and review

Preview service: `dev.uni.joe-creations-preview`, Caddy on loopback port 4189, serving this worktree's `_site`. Private Tailscale HTTPS endpoint: port 8446, `/joe/creations/`. This is a review preview, not a deployment to unforced.org.

Validation: full Eleventy build; all 70 previews exercised in Chromium, desktop and mobile checks, source asset/link checks, and comparison with original Flash renders. See session log for final validation state and any remaining limits. The original site was inspected through an emulator; that is not a claim of compatibility testing in the discontinued Adobe plugin.

## Direction for /joe

I would make `/joe/` an introduction to a whole life, with the complete book remaining immediately accessible and all existing chapter links preserved.

1. **Joe, in his own words.** A short introduction using established biographical facts, a photograph, and links to the book and restored portfolio. Keep the warmth and humor already present in his writing.
2. **What he made.** A curated view of the houses, spaces, woodworking, and gardens. Pair actual project photographs with related passages, clearly distinguishing Joe's words from new captions. Link through to the restored site as an artifact with its own visual identity. Confirm project names and dates before enriching filename-derived labels.
3. **How he practiced.** Tai Ji, attention, working with material, family, and relationship, grounded in the book and Aaron's essays. A natural bridge is `joe/Vision and finishing well.docx`: Joe explicitly describes the book as his largest project since Big Song Music House and ties both to the same care in making things. That document also includes a historical fundraiser, which should be contextualized as history if excerpted.
4. **The book.** Retain the full reader, EPUB, chapter navigation, family images, and listening option. Compare the newly preserved INDD with the existing book before changing text or artwork. Complete and assess audio separately; the existing manifest remains partial.
5. **Remembering Joe.** Aaron's birthday letter and Laurie's epilogue provide an existing foundation. Stories from Suzy and others could grow this section with clear authorship and context.

The next editorial step is a small set of representative project/photo/passage pairings for Aaron to review. This proposal does not silently publish newly recovered correspondence, fundraising instructions, or manuscripts.
