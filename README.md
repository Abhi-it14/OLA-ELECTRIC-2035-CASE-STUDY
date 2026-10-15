# Ola Commute: A 2035 Product Strategy Case Study

> **India doesn't need another vehicle. It needs a better commute.**

A 5-page, consulting-style case study for the Ola Electric product strategy assignment:

*"Imagine it is 2035. Ola wants to build a mobility product that 100 million Indians use for their daily commute. It cannot be a scooter or motorcycle. What do you build?"*

**Answer:** **Ola Commute**, a recurring, multimodal commute service for metro-city weekday commuters. Mass transit stays the backbone, and Ola guarantees the first and last mile with pooled electric feeders and an automatic fallback ride.

📄 **Read the report:** [`Ola_Commute_Case_Study_2035.pdf`](Ola_Commute_Case_Study_2035.pdf)

---

## What's inside

| Page | Headline | Covers |
|------|----------|--------|
| 1 | India doesn't need another vehicle. It needs a better commute. | Answer, headline numbers, 2035 assumptions, the case in seven answers |
| 2 | The pain is the connection between modes, not a lack of transport | Target user, problem, why it matters in 2035, scale of 100M |
| 3 | Ola Commute: one booking, one promise, multiple modes | Product, user journey, six key features, strategic boundary |
| 4 | The moat is coordination and density, not the vehicle itself | Alternatives scored, mode comparison, why Ola |
| 5 | Density first: win one corridor, then a city, then 60-80 cities | MVP roadmap, path to 100M, what must be true, success metrics, kill criteria |

## Repository contents

```
.
├── Ola_Commute_Case_Study_2035.pdf   # Final report (5 pages, A4 landscape)
├── build.py                          # Script that generates the PDF
└── README.md
```

## Rebuilding the PDF

The report is generated with [ReportLab](https://www.reportlab.com/). Every chart, icon and layout element is drawn as vector graphics, so no image files are needed.

```bash
pip install reportlab
python build.py
```

**Fonts:** `build.py` expects these TrueType files. Edit the `GF` and `LF` paths near the top of the script to point at them on your machine:

- [Poppins](https://fonts.google.com/specimen/Poppins) (Regular, Medium, Bold) for headings
- [Liberation Sans](https://github.com/liberationfonts/liberation-fonts) (Regular, Bold, Italic, Bold Italic) for body text

## Customising

- **Colours:** change the named constants at the top of `build.py` (`NAVY`, `LIME`, `AMBER`, `GREY_L` and so on).
- **Fonts:** change the `registerFont` lines at the top of `build.py`.
- **Content:** each page is its own function (`page1` to `page5`), so text and numbers can be edited in place.

## Notes on the data

- Weighted concept scores on page 4 are **recalculated from the stated criteria weights**. They differ slightly from the original draft, and the ranking is unchanged.
- Items marked **[NEEDS SOURCE]** in the report are open data gaps: the total-population figure (year and publisher), the beachhead segment size, and the on-time arrival and fallback trigger rate targets.
- The unit economics (40 / 31 / 9) are illustrative target-state figures, and the currency unit is still to be confirmed.
- App screens on page 3 are illustrative concept mock-ups, not a live product.

## Sources

World Bank (*Financing India's Urban Infrastructure Needs*; *Designing Public Transport in India That Works for All*), PIB/MoHUA (2025 Metro Rail review; PM-eBus Sewa), TomTom Traffic Index 2025, NITI Aayog (*Scenarios Towards Viksit Bharat and Net Zero: Transport*), and Ola Electric materials (MoveOS 5 announcement, DRHP, investor relations).

## Disclaimer

This is an independent candidate submission for an assignment. It is not affiliated with or endorsed by Ola Electric.
