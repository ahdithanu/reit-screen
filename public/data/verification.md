# verification.md

Run as_of 2026-11-09. Names in this run: SL Green, Cousins Properties, JBG Smith, Piedmont Office, Office Properties Income Trust, Empire State Realty Trust, BXP, CBL & Associates, Simon Property Group, Brixmor, Acadia Realty, Kite Realty, Vornado Realty Trust, Kilroy Realty, Highwoods Properties, Douglas Emmett, Hudson Pacific Properties, Brandywine Realty Trust, Regency Centers, Kimco Realty, Federal Realty, Macerich, Tanger, Phillips Edison.
Raw diffs are printed in full, not summarized.

## 1. Pipeline control (OPI must be ACT NOW)

**PASS**: expected ACT NOW, got **ACT NOW** (hard trigger: 1.03, NT 10-Q)

## 2. Cross-extraction: companyfacts (A) vs frames CY2025Q4I (B)

Checks the plumbing (two SEC endpoints over the same filings), not the filer.

| name | tag | A value | A accn / reason | B value | B accn / reason | same |
|---|---|---:|---|---:|---|---|
| SL Green | LTDMat…InNextTwelveMonths | 655,148,000 | 0001628280-26-008669 (10-K) | 655,148,000 | 0001628280-26-008669 | yes |
| SL Green | LTDMat…InYearTwo | 2,569,277,000 | 0001628280-26-008669 (10-K) | 2,569,277,000 | 0001628280-26-008669 | yes |
| SL Green | LTDMat…InYearThree | 284,550,000 | 0001628280-26-008669 (10-K) | 284,550,000 | 0001628280-26-008669 | yes |
| SL Green | LTDMat…InYearFour | 177,000,000 | 0001628280-26-008669 (10-K) | 177,000,000 | 0001628280-26-008669 | yes |
| SL Green | LTDMat…InYearFive | 0 | 0001628280-26-008669 (10-K) | 0 | 0001628280-26-008669 | yes |
| SL Green | LTDMat…AfterYearFive | 358,524,000 | 0001628280-26-008669 (10-K) | 358,524,000 | 0001628280-26-008669 | yes |
| SL Green | CashAndCashEquivalentsAtCarryingValue | 155,747,000 | 0001628280-26-029075 (10-Q) | 155,747,000 | 0001628280-26-029075 | yes |
| SL Green | LongTermDebt | n/a | no 10-K/10-Q instant at 2025-12-31 | n/a | cik not in frame | both missing |
| Cousins Properties | LTDMat…InNextTwelveMonths | 870,127,000 | 0000025232-26-000014 (10-K) | 870,127,000 | 0000025232-26-000014 | yes |
| Cousins Properties | LTDMat…InYearTwo | 341,000,000 | 0000025232-26-000014 (10-K) | 341,000,000 | 0000025232-26-000014 | yes |
| Cousins Properties | LTDMat…InYearThree | 250,000,000 | 0000025232-26-000014 (10-K) | 250,000,000 | 0000025232-26-000014 | yes |
| Cousins Properties | LTDMat…InYearFour | 275,000,000 | 0000025232-26-000014 (10-K) | 275,000,000 | 0000025232-26-000014 | yes |
| Cousins Properties | LTDMat…InYearFive | 500,000,000 | 0000025232-26-000014 (10-K) | 500,000,000 | 0000025232-26-000014 | yes |
| Cousins Properties | LTDMat…AfterYearFive | 1,121,000,000 | 0000025232-26-000014 (10-K) | 1,121,000,000 | 0000025232-26-000014 | yes |
| Cousins Properties | CashAndCashEquivalentsAtCarryingValue | 5,720,000 | 0000025232-26-000079 (10-Q) | 5,720,000 | 0000025232-26-000079 | yes |
| Cousins Properties | LongTermDebt | 3,340,815,000 | 0000025232-26-000079 (10-Q) | 3,340,815,000 | 0000025232-26-000079 | yes |
| JBG Smith | LTDMat…InNextTwelveMonths | 170,820,000 | 0001104659-26-016450 (10-K) | 170,820,000 | 0001104659-26-016450 | yes |
| JBG Smith | LTDMat…InYearTwo | 676,303,000 | 0001104659-26-016450 (10-K) | 676,303,000 | 0001104659-26-016450 | yes |
| JBG Smith | LTDMat…InYearThree | 610,147,000 | 0001104659-26-016450 (10-K) | 610,147,000 | 0001104659-26-016450 | yes |
| JBG Smith | LTDMat…InYearFour | 278,987,000 | 0001104659-26-016450 (10-K) | 278,987,000 | 0001104659-26-016450 | yes |
| JBG Smith | LTDMat…InYearFive | 810,332,000 | 0001104659-26-016450 (10-K) | 810,332,000 | 0001104659-26-016450 | yes |
| JBG Smith | LTDMat…AfterYearFive | n/a | no 10-K/10-Q instant at 2025-12-31 | n/a | cik not in frame | both missing |
| JBG Smith | CashAndCashEquivalentsAtCarryingValue | 75,270,000 | 0001104659-26-123567 (10-Q) | 75,270,000 | 0001104659-26-123567 | yes |
| JBG Smith | LongTermDebt | n/a | no 10-K/10-Q instant at 2025-12-31 | n/a | cik not in frame | both missing |
| Piedmont Office | LTDMat…InNextTwelveMonths | 3,433,000 | 0001042776-26-000012 (10-K) | 3,433,000 | 0001042776-26-000012 | yes |
| Piedmont Office | LTDMat…InYearTwo | 328,894,000 | 0001042776-26-000012 (10-K) | 328,894,000 | 0001042776-26-000012 | yes |
| Piedmont Office | LTDMat…InYearThree | 515,753,000 | 0001042776-26-000012 (10-K) | 515,753,000 | 0001042776-26-000012 | yes |
| Piedmont Office | LTDMat…InYearFour | 400,000,000 | 0001042776-26-000012 (10-K) | 400,000,000 | 0001042776-26-000012 | yes |
| Piedmont Office | LTDMat…InYearFive | 300,000,000 | 0001042776-26-000012 (10-K) | 300,000,000 | 0001042776-26-000012 | yes |
| Piedmont Office | LTDMat…AfterYearFive | 700,000,000 | 0001042776-26-000012 (10-K) | 700,000,000 | 0001042776-26-000012 | yes |
| Piedmont Office | CashAndCashEquivalentsAtCarryingValue | 731,000 | 0001042776-26-000071 (10-Q) | 731,000 | 0001042776-26-000071 | yes |
| Piedmont Office | LongTermDebt | 2,224,712,000 | 0001042776-26-000071 (10-Q) | 2,224,712,000 | 0001042776-26-000071 | yes |
| Office Properties Income Trust | LTDMat…InNextTwelveMonths | 144,154,000 | 0001456772-26-000022 (10-K) | 144,154,000 | 0001456772-26-000022 | yes |
| Office Properties Income Trust | LTDMat…InYearTwo | 921,300,000 | 0001456772-26-000022 (10-K) | 921,300,000 | 0001456772-26-000022 | yes |
| Office Properties Income Trust | LTDMat…InYearThree | 123,487,000 | 0001456772-26-000022 (10-K) | 123,487,000 | 0001456772-26-000022 | yes |
| Office Properties Income Trust | LTDMat…InYearFour | 910,278,000 | 0001456772-26-000022 (10-K) | 910,278,000 | 0001456772-26-000022 | yes |
| Office Properties Income Trust | LTDMat…InYearFive | 14,739,000 | 0001456772-26-000022 (10-K) | 14,739,000 | 0001456772-26-000022 | yes |
| Office Properties Income Trust | LTDMat…AfterYearFive | 317,656,000 | 0001456772-26-000022 (10-K) | 317,656,000 | 0001456772-26-000022 | yes |
| Office Properties Income Trust | CashAndCashEquivalentsAtCarryingValue | 29,486,000 | 0001456772-26-000023 (10-Q) | 29,486,000 | 0001456772-26-000023 | yes |
| Office Properties Income Trust | LongTermDebt | 2,408,626,000 | 0001456772-26-000022 (10-K) | 2,408,626,000 | 0001456772-26-000022 | yes |
| Empire State Realty Trust | LTDMat…InNextTwelveMonths | 53,958,000 | 0001541401-26-000008 (10-K) | 53,958,000 | 0001541401-26-000008 | yes |
| Empire State Realty Trust | LTDMat…InYearTwo | 159,276,000 | 0001541401-26-000008 (10-K) | 159,276,000 | 0001541401-26-000008 | yes |
| Empire State Realty Trust | LTDMat…InYearThree | 149,646,000 | 0001541401-26-000008 (10-K) | 149,646,000 | 0001541401-26-000008 | yes |
| Empire State Realty Trust | LTDMat…InYearFour | 398,890,000 | 0001541401-26-000008 (10-K) | 398,890,000 | 0001541401-26-000008 | yes |
| Empire State Realty Trust | LTDMat…InYearFive | 513,111,000 | 0001541401-26-000008 (10-K) | 513,111,000 | 0001541401-26-000008 | yes |
| Empire State Realty Trust | LTDMat…AfterYearFive | 1,114,130,000 | 0001541401-26-000008 (10-K) | 1,114,130,000 | 0001541401-26-000008 | yes |
| Empire State Realty Trust | CashAndCashEquivalentsAtCarryingValue | 132,657,000 | 0001541401-26-000033 (10-Q) | 132,657,000 | 0001541401-26-000033 | yes |
| Empire State Realty Trust | LongTermDebt | n/a | no 10-K/10-Q instant at 2025-12-31 | n/a | cik not in frame | both missing |
| BXP | LTDMat…InNextTwelveMonths | n/a | no 10-K/10-Q instant at 2025-12-31 | n/a | cik not in frame | both missing |
| BXP | LTDMat…InYearTwo | n/a | no 10-K/10-Q instant at 2025-12-31 | n/a | cik not in frame | both missing |
| BXP | LTDMat…InYearThree | n/a | no 10-K/10-Q instant at 2025-12-31 | n/a | cik not in frame | both missing |
| BXP | LTDMat…InYearFour | n/a | no 10-K/10-Q instant at 2025-12-31 | n/a | cik not in frame | both missing |
| BXP | LTDMat…InYearFive | n/a | no 10-K/10-Q instant at 2025-12-31 | n/a | cik not in frame | both missing |
| BXP | LTDMat…AfterYearFive | n/a | no 10-K/10-Q instant at 2025-12-31 | n/a | cik not in frame | both missing |
| BXP | CashAndCashEquivalentsAtCarryingValue | 1,478,206,000 | 0001037540-26-000034 (10-Q) | 1,478,206,000 | 0001037540-26-000034 | yes |
| BXP | LongTermDebt | n/a | no 10-K/10-Q instant at 2025-12-31 | n/a | cik not in frame | both missing |
| CBL & Associates | LTDMat…InNextTwelveMonths | 1,281,692,000 | 0001193125-26-087049 (10-K) | 1,281,692,000 | 0001193125-26-087049 | yes |
| CBL & Associates | LTDMat…InYearTwo | 11,195 | 0001193125-26-087049 (10-K) | 11,195 | 0001193125-26-087049 | yes |
| CBL & Associates | LTDMat…InYearThree | 134,781,000 | 0001193125-26-087049 (10-K) | 134,781,000 | 0001193125-26-087049 | yes |
| CBL & Associates | LTDMat…InYearFour | 7,939,000 | 0001193125-26-087049 (10-K) | 7,939,000 | 0001193125-26-087049 | yes |
| CBL & Associates | LTDMat…InYearFive | 740,144,000 | 0001193125-26-087049 (10-K) | 740,144,000 | 0001193125-26-087049 | yes |
| CBL & Associates | LTDMat…AfterYearFive | 59,831,000 | 0001193125-26-087049 (10-K) | 59,831,000 | 0001193125-26-087049 | yes |
| CBL & Associates | CashAndCashEquivalentsAtCarryingValue | 42,287,000 | 0001193125-26-339651 (10-Q) | 42,287,000 | 0001193125-26-339651 | yes |
| CBL & Associates | LongTermDebt | 2,170,785,000 | 0001193125-26-339651 (10-Q) | 2,170,785,000 | 0001193125-26-339651 | yes |
| Simon Property Group | LTDMat…InNextTwelveMonths | 5,905,606,000 | 0001104659-26-019419 (10-K) | 5,905,606,000 | 0001104659-26-019419 | yes |
| Simon Property Group | LTDMat…InYearTwo | 3,936,773,000 | 0001104659-26-019419 (10-K) | 3,936,773,000 | 0001104659-26-019419 | yes |
| Simon Property Group | LTDMat…InYearThree | 2,296,651,000 | 0001104659-26-019419 (10-K) | 2,296,651,000 | 0001104659-26-019419 | yes |
| Simon Property Group | LTDMat…InYearFour | 2,940,031,000 | 0001104659-26-019419 (10-K) | 2,940,031,000 | 0001104659-26-019419 | yes |
| Simon Property Group | LTDMat…InYearFive | 1,657,864,000 | 0001104659-26-019419 (10-K) | 1,657,864,000 | 0001104659-26-019419 | yes |
| Simon Property Group | LTDMat…AfterYearFive | 11,858,614,000 | 0001104659-26-019419 (10-K) | 11,858,614,000 | 0001104659-26-019419 | yes |
| Simon Property Group | CashAndCashEquivalentsAtCarryingValue | 823,147,000 | 0001104659-26-123591 (10-Q) | 823,147,000 | 0001104659-26-123591 | yes |
| Simon Property Group | LongTermDebt | 28,430,175,000 | 0001104659-26-123591 (10-Q) | 28,430,175,000 | 0001104659-26-123591 | yes |
| Brixmor | LTDMat…InNextTwelveMonths | 607,542,000 | 0001581068-26-000007 (10-K) | 607,542,000 | 0001581068-26-000007 | yes |
| Brixmor | LTDMat…InYearTwo | 400,000,000 | 0001581068-26-000007 (10-K) | 400,000,000 | 0001581068-26-000007 | yes |
| Brixmor | LTDMat…InYearThree | 357,708,000 | 0001581068-26-000007 (10-K) | 357,708,000 | 0001581068-26-000007 | yes |
| Brixmor | LTDMat…InYearFour | 753,203,000 | 0001581068-26-000007 (10-K) | 753,203,000 | 0001581068-26-000007 | yes |
| Brixmor | LTDMat…InYearFive | 1,300,000,000 | 0001581068-26-000007 (10-K) | 1,300,000,000 | 0001581068-26-000007 | yes |
| Brixmor | LTDMat…AfterYearFive | 2,100,000,000 | 0001581068-26-000007 (10-K) | 2,100,000,000 | 0001581068-26-000007 | yes |
| Brixmor | CashAndCashEquivalentsAtCarryingValue | 334,422,000 | 0001581068-26-000031 (10-Q) | 334,422,000 | 0001581068-26-000031 | yes |
| Brixmor | LongTermDebt | 5,494,753,000 | 0001581068-26-000031 (10-Q) | 5,494,753,000 | 0001581068-26-000031 | yes |
| Acadia Realty | LTDMat…InNextTwelveMonths | 292,287,000 | 0001193125-26-051677 (10-K) | 292,287,000 | 0001193125-26-051677 | yes |
| Acadia Realty | LTDMat…InYearTwo | 309,638,000 | 0001193125-26-051677 (10-K) | 309,638,000 | 0001193125-26-051677 | yes |
| Acadia Realty | LTDMat…InYearThree | 845,235,000 | 0001193125-26-051677 (10-K) | 845,235,000 | 0001193125-26-051677 | yes |
| Acadia Realty | LTDMat…InYearFour | 98,292,000 | 0001193125-26-051677 (10-K) | 98,292,000 | 0001193125-26-051677 | yes |
| Acadia Realty | LTDMat…InYearFive | 326,850,000 | 0001193125-26-051677 (10-K) | 326,850,000 | 0001193125-26-051677 | yes |
| Acadia Realty | LTDMat…AfterYearFive | 1,065,000 | 0001193125-26-051677 (10-K) | 1,065,000 | 0001193125-26-051677 | yes |
| Acadia Realty | CashAndCashEquivalentsAtCarryingValue | 38,818,000 | 0001193125-26-443763 (10-Q) | 38,818,000 | 0001193125-26-443763 | yes |
| Acadia Realty | LongTermDebt | 1,862,906,000 | 0001193125-26-443763 (10-Q) | 1,862,906,000 | 0001193125-26-443763 | yes |
| Kite Realty | LTDMat…InNextTwelveMonths | 415,181,000 | 0001286043-26-000009 (10-K) | 415,181,000 | 0001286043-26-000009 | yes |
| Kite Realty | LTDMat…InYearTwo | 522,568,000 | 0001286043-26-000009 (10-K) | 522,568,000 | 0001286043-26-000009 | yes |
| Kite Realty | LTDMat…InYearThree | 187,943,000 | 0001286043-26-000009 (10-K) | 187,943,000 | 0001286043-26-000009 | yes |
| Kite Realty | LTDMat…InYearFour | 403,474,000 | 0001286043-26-000009 (10-K) | 403,474,000 | 0001286043-26-000009 | yes |
| Kite Realty | LTDMat…InYearFive | 403,036,000 | 0001286043-26-000009 (10-K) | 403,036,000 | 0001286043-26-000009 | yes |
| Kite Realty | LTDMat…AfterYearFive | 1,095,735,000 | 0001286043-26-000009 (10-K) | 1,095,735,000 | 0001286043-26-000009 | yes |
| Kite Realty | CashAndCashEquivalentsAtCarryingValue | 36,761,000 | 0001286043-26-000058 (10-Q) | 36,761,000 | 0001286043-26-000058 | yes |
| Kite Realty | LongTermDebt | 3,025,478,000 | 0001286043-26-000058 (10-Q) | 3,025,478,000 | 0001286043-26-000058 | yes |
| Vornado Realty Trust | LTDMat…InNextTwelveMonths | n/a | tag not reported by filer | n/a | cik not in frame | both missing |
| Vornado Realty Trust | LTDMat…InYearTwo | n/a | tag not reported by filer | n/a | cik not in frame | both missing |
| Vornado Realty Trust | LTDMat…InYearThree | n/a | tag not reported by filer | n/a | cik not in frame | both missing |
| Vornado Realty Trust | LTDMat…InYearFour | n/a | tag not reported by filer | n/a | cik not in frame | both missing |
| Vornado Realty Trust | LTDMat…InYearFive | n/a | tag not reported by filer | n/a | cik not in frame | both missing |
| Vornado Realty Trust | LTDMat…AfterYearFive | n/a | tag not reported by filer | n/a | cik not in frame | both missing |
| Vornado Realty Trust | CashAndCashEquivalentsAtCarryingValue | 840,850,000 | 0000899689-26-000046 (10-Q) | 840,850,000 | 0000899689-26-000046 | yes |
| Vornado Realty Trust | LongTermDebt | 2,264,959,000 | 0000899689-26-000046 (10-Q) | 2,264,959,000 | 0000899689-26-000046 | yes |
| Kilroy Realty | LTDMat…InNextTwelveMonths | 601,317,000 | 0001628280-26-007051 (10-K) | 601,317,000 | 0001628280-26-007051 | yes |
| Kilroy Realty | LTDMat…InYearTwo | 249,125,000 | 0001628280-26-007051 (10-K) | 249,125,000 | 0001628280-26-007051 | yes |
| Kilroy Realty | LTDMat…InYearThree | n/a | tag not reported by filer | n/a | cik not in frame | both missing |
| Kilroy Realty | LTDMat…InYearFour | n/a | tag not reported by filer | n/a | cik not in frame | both missing |
| Kilroy Realty | LTDMat…InYearFive | n/a | tag not reported by filer | n/a | cik not in frame | both missing |
| Kilroy Realty | LTDMat…AfterYearFive | 2,400,000,000 | 0001628280-26-007051 (10-K) | 2,400,000,000 | 0001628280-26-007051 | yes |
| Kilroy Realty | CashAndCashEquivalentsAtCarryingValue | 179,316,000 | 0001628280-26-028013 (10-Q) | 179,316,000 | 0001628280-26-028013 | yes |
| Kilroy Realty | LongTermDebt | n/a | no 10-K/10-Q instant at 2025-12-31 | n/a | cik not in frame | both missing |
| Highwoods Properties | LTDMat…InNextTwelveMonths | 6,682,000 | 0000921082-26-000005 (10-K) | 6,682,000 | 0000921082-26-000005 | yes |
| Highwoods Properties | LTDMat…InYearTwo | 458,736,000 | 0000921082-26-000005 (10-K) | 458,736,000 | 0000921082-26-000005 | yes |
| Highwoods Properties | LTDMat…InYearThree | 723,928,000 | 0000921082-26-000005 (10-K) | 723,928,000 | 0000921082-26-000005 | yes |
| Highwoods Properties | LTDMat…InYearFour | 717,027,000 | 0000921082-26-000005 (10-K) | 717,027,000 | 0000921082-26-000005 | yes |
| Highwoods Properties | LTDMat…InYearFive | 404,662,000 | 0000921082-26-000005 (10-K) | 404,662,000 | 0000921082-26-000005 | yes |
| Highwoods Properties | LTDMat…AfterYearFive | 1,259,119,000 | 0000921082-26-000005 (10-K) | 1,259,119,000 | 0000921082-26-000005 | yes |
| Highwoods Properties | CashAndCashEquivalentsAtCarryingValue | 27,358,000 | 0000921082-26-000035 (10-Q) | 27,358,000 | 0000921082-26-000035 | yes |
| Highwoods Properties | LongTermDebt | n/a | tag not reported by filer | n/a | cik not in frame | both missing |
| Douglas Emmett | LTDMat…InNextTwelveMonths | n/a | no 10-K/10-Q instant at 2025-12-31 | n/a | cik not in frame | both missing |
| Douglas Emmett | LTDMat…InYearTwo | n/a | no 10-K/10-Q instant at 2025-12-31 | n/a | cik not in frame | both missing |
| Douglas Emmett | LTDMat…InYearThree | n/a | no 10-K/10-Q instant at 2025-12-31 | n/a | cik not in frame | both missing |
| Douglas Emmett | LTDMat…InYearFour | n/a | no 10-K/10-Q instant at 2025-12-31 | n/a | cik not in frame | both missing |
| Douglas Emmett | LTDMat…InYearFive | n/a | no 10-K/10-Q instant at 2025-12-31 | n/a | cik not in frame | both missing |
| Douglas Emmett | LTDMat…AfterYearFive | n/a | no 10-K/10-Q instant at 2025-12-31 | n/a | cik not in frame | both missing |
| Douglas Emmett | CashAndCashEquivalentsAtCarryingValue | 340,789,000 | 0001364250-26-000057 (10-Q) | 340,789,000 | 0001364250-26-000057 | yes |
| Douglas Emmett | LongTermDebt | 5,548,870,000 | 0001364250-26-000057 (10-Q) | 5,548,870,000 | 0001364250-26-000057 | yes |
| Hudson Pacific Properties | LTDMat…InNextTwelveMonths | n/a | no 10-K/10-Q instant at 2025-12-31 | n/a | cik not in frame | both missing |
| Hudson Pacific Properties | LTDMat…InYearTwo | n/a | no 10-K/10-Q instant at 2025-12-31 | n/a | cik not in frame | both missing |
| Hudson Pacific Properties | LTDMat…InYearThree | n/a | no 10-K/10-Q instant at 2025-12-31 | n/a | cik not in frame | both missing |
| Hudson Pacific Properties | LTDMat…InYearFour | n/a | no 10-K/10-Q instant at 2025-12-31 | n/a | cik not in frame | both missing |
| Hudson Pacific Properties | LTDMat…InYearFive | n/a | no 10-K/10-Q instant at 2025-12-31 | n/a | cik not in frame | both missing |
| Hudson Pacific Properties | LTDMat…AfterYearFive | n/a | no 10-K/10-Q instant at 2025-12-31 | n/a | cik not in frame | both missing |
| Hudson Pacific Properties | CashAndCashEquivalentsAtCarryingValue | 138,358,000 | 0001482512-26-000050 (10-Q) | 138,358,000 | 0001482512-26-000050 | yes |
| Hudson Pacific Properties | LongTermDebt | n/a | no 10-K/10-Q instant at 2025-12-31 | n/a | cik not in frame | both missing |
| Brandywine Realty Trust | LTDMat…InNextTwelveMonths | 178,014,000 | 0000790816-26-000008 (10-K) | 178,014,000 | 0000790816-26-000008 | yes |
| Brandywine Realty Trust | LTDMat…InYearTwo | 700,000,000 | 0000790816-26-000008 (10-K) | 700,000,000 | 0000790816-26-000008 | yes |
| Brandywine Realty Trust | LTDMat…InYearThree | 350,000,000 | 0000790816-26-000008 (10-K) | 350,000,000 | 0000790816-26-000008 | yes |
| Brandywine Realty Trust | LTDMat…InYearFour | 900,000,000 | 0000790816-26-000008 (10-K) | 900,000,000 | 0000790816-26-000008 | yes |
| Brandywine Realty Trust | LTDMat…InYearFive | 0 | 0000790816-26-000008 (10-K) | 0 | 0000790816-26-000008 | yes |
| Brandywine Realty Trust | LTDMat…AfterYearFive | 435,934,000 | 0000790816-26-000008 (10-K) | 435,934,000 | 0000790816-26-000008 | yes |
| Brandywine Realty Trust | CashAndCashEquivalentsAtCarryingValue | 32,284,000 | 0000790816-26-000045 (10-Q) | 32,284,000 | 0000790816-26-000045 | yes |
| Brandywine Realty Trust | LongTermDebt | 2,556,862,000 | 0000790816-26-000045 (10-Q) | 2,556,862,000 | 0000790816-26-000045 | yes |
| Regency Centers | LTDMat…InNextTwelveMonths | 360,684,000 | 0001193125-26-051668 (10-K) | 360,684,000 | 0001193125-26-051668 | yes |
| Regency Centers | LTDMat…InYearTwo | 757,609,000 | 0001193125-26-051668 (10-K) | 757,609,000 | 0001193125-26-051668 | yes |
| Regency Centers | LTDMat…InYearThree | 480,304,000 | 0001193125-26-051668 (10-K) | 480,304,000 | 0001193125-26-051668 | yes |
| Regency Centers | LTDMat…InYearFour | 527,739,000 | 0001193125-26-051668 (10-K) | 527,739,000 | 0001193125-26-051668 | yes |
| Regency Centers | LTDMat…InYearFive | 607,608,000 | 0001193125-26-051668 (10-K) | 607,608,000 | 0001193125-26-051668 | yes |
| Regency Centers | LTDMat…AfterYearFive | 2,064,887,000 | 0001193125-26-051668 (10-K) | 2,064,887,000 | 0001193125-26-051668 | yes |
| Regency Centers | CashAndCashEquivalentsAtCarryingValue | n/a | no 10-K/10-Q instant at 2025-12-31 | n/a | cik not in frame | both missing |
| Regency Centers | LongTermDebt | 4,739,301,000 | 0001193125-26-203537 (10-Q) | 4,739,301,000 | 0001193125-26-203537 | yes |
| Kimco Realty | LTDMat…InNextTwelveMonths | n/a | no 10-K/10-Q instant at 2025-12-31 | n/a | cik not in frame | both missing |
| Kimco Realty | LTDMat…InYearTwo | n/a | no 10-K/10-Q instant at 2025-12-31 | n/a | cik not in frame | both missing |
| Kimco Realty | LTDMat…InYearThree | n/a | no 10-K/10-Q instant at 2025-12-31 | n/a | cik not in frame | both missing |
| Kimco Realty | LTDMat…InYearFour | n/a | no 10-K/10-Q instant at 2025-12-31 | n/a | cik not in frame | both missing |
| Kimco Realty | LTDMat…InYearFive | n/a | no 10-K/10-Q instant at 2025-12-31 | n/a | cik not in frame | both missing |
| Kimco Realty | LTDMat…AfterYearFive | n/a | no 10-K/10-Q instant at 2025-12-31 | n/a | cik not in frame | both missing |
| Kimco Realty | CashAndCashEquivalentsAtCarryingValue | 211,648,000 | 0001193125-26-331817 (10-Q) | 211,648,000 | 0001193125-26-331817 | yes |
| Kimco Realty | LongTermDebt | 7,718,700,000 | 0001193125-26-060760 (10-K) | 7,718,700,000 | 0001193125-26-060760 | yes |
| Federal Realty | LTDMat…InNextTwelveMonths | 655,595,000 | 0000034903-26-000017 (10-K) | 655,595,000 | 0000034903-26-000017 | yes |
| Federal Realty | LTDMat…InYearTwo | 1,003,319,000 | 0000034903-26-000017 (10-K) | 1,003,319,000 | 0000034903-26-000017 | yes |
| Federal Realty | LTDMat…InYearThree | 1,157,511,000 | 0000034903-26-000017 (10-K) | 1,157,511,000 | 0000034903-26-000017 | yes |
| Federal Realty | LTDMat…InYearFour | 945,434,000 | 0000034903-26-000017 (10-K) | 945,434,000 | 0000034903-26-000017 | yes |
| Federal Realty | LTDMat…InYearFive | 400,684,000 | 0000034903-26-000017 (10-K) | 400,684,000 | 0000034903-26-000017 | yes |
| Federal Realty | LTDMat…AfterYearFive | 801,059,000 | 0000034903-26-000017 (10-K) | 801,059,000 | 0000034903-26-000017 | yes |
| Federal Realty | CashAndCashEquivalentsAtCarryingValue | 107,415,000 | 0000034903-26-000026 (10-Q) | 107,415,000 | 0000034903-26-000026 | yes |
| Federal Realty | LongTermDebt | 4,963,602,000 | 0000034903-26-000017 (10-K) | 4,963,602,000 | 0000034903-26-000017 | yes |
| Macerich | LTDMat…InNextTwelveMonths | n/a | tag not reported by filer | n/a | cik not in frame | both missing |
| Macerich | LTDMat…InYearTwo | n/a | tag not reported by filer | n/a | cik not in frame | both missing |
| Macerich | LTDMat…InYearThree | n/a | tag not reported by filer | n/a | cik not in frame | both missing |
| Macerich | LTDMat…InYearFour | n/a | tag not reported by filer | n/a | cik not in frame | both missing |
| Macerich | LTDMat…InYearFive | n/a | tag not reported by filer | n/a | cik not in frame | both missing |
| Macerich | LTDMat…AfterYearFive | n/a | tag not reported by filer | n/a | cik not in frame | both missing |
| Macerich | CashAndCashEquivalentsAtCarryingValue | 280,246,000 | 0000912242-26-000045 (10-Q) | 280,246,000 | 0000912242-26-000045 | yes |
| Macerich | LongTermDebt | 5,068,946,000 | 0000912242-26-000045 (10-Q) | 5,068,946,000 | 0000912242-26-000045 | yes |
| Tanger | LTDMat…InNextTwelveMonths | n/a | tag not reported by filer | n/a | cik not in frame | both missing |
| Tanger | LTDMat…InYearTwo | n/a | tag not reported by filer | n/a | cik not in frame | both missing |
| Tanger | LTDMat…InYearThree | n/a | tag not reported by filer | n/a | cik not in frame | both missing |
| Tanger | LTDMat…InYearFour | n/a | tag not reported by filer | n/a | cik not in frame | both missing |
| Tanger | LTDMat…InYearFive | n/a | tag not reported by filer | n/a | cik not in frame | both missing |
| Tanger | LTDMat…AfterYearFive | n/a | tag not reported by filer | n/a | cik not in frame | both missing |
| Tanger | CashAndCashEquivalentsAtCarryingValue | 18,133,000 | 0001628280-26-071352 (10-Q) | 18,133,000 | 0001628280-26-071352 | yes |
| Tanger | LongTermDebt | 1,596,821,000 | 0001628280-26-071352 (10-Q) | 1,596,821,000 | 0001628280-26-071352 | yes |
| Phillips Edison | LTDMat…InNextTwelveMonths | 163,654,000 | 0001476204-26-000005 (10-K) | 163,654,000 | 0001476204-26-000005 | yes |
| Phillips Edison | LTDMat…InYearTwo | 523,595,000 | 0001476204-26-000005 (10-K) | 523,595,000 | 0001476204-26-000005 | yes |
| Phillips Edison | LTDMat…InYearThree | 17,367,000 | 0001476204-26-000005 (10-K) | 17,367,000 | 0001476204-26-000005 | yes |
| Phillips Edison | LTDMat…InYearFour | 92,805,000 | 0001476204-26-000005 (10-K) | 92,805,000 | 0001476204-26-000005 | yes |
| Phillips Edison | LTDMat…InYearFive | 200,844,000 | 0001476204-26-000005 (10-K) | 200,844,000 | 0001476204-26-000005 | yes |
| Phillips Edison | LTDMat…AfterYearFive | 1,403,400,000 | 0001476204-26-000005 (10-K) | 1,403,400,000 | 0001476204-26-000005 | yes |
| Phillips Edison | CashAndCashEquivalentsAtCarryingValue | 3,544,000 | 0001476204-26-000054 (10-Q) | 3,544,000 | 0001476204-26-000054 | yes |
| Phillips Edison | LongTermDebt | 2,375,328,000 | 0001476204-26-000054 (10-Q) | 2,375,328,000 | 0001476204-26-000054 | yes |

**Differences: 0**

Side A uses the frames selection rule: the most recently filed 10-K or 10-Q fact for the instant. Until 2026-11-09 side A read 10-K facts only; rows that differed only because of that are listed under Conflicts and gaps as RESOLVED.


## 3. Spot check against 10-K text

### SL Green
Source: https://www.sec.gov/Archives/edgar/data/1040971/000162828026008669/slg-20251231.htm

Method: the inline-XBRL facts rendered *inside the 10-K document* (dimensionless context, instant 2025-12-31), displayed number × 10^scale, compared with the companyfacts value.

| bucket | tag | extracted (companyfacts) | 10-K displayed → USD | shown text | diff | note |
|---|---|---:|---:|---|---:|---|
| y1_2026 | …InNextTwelveMonths | 655,148,000 | 655,148,000 | 655,148 (scale 3) | 0 |  |
| y2_2027 | …InYearTwo | 2,569,277,000 | 2,569,277,000 | 2,569,277 (scale 3) | 0 |  |
| y3_2028 | …InYearThree | 284,550,000 | 284,550,000 | 284,550 (scale 3) | 0 |  |
| y4_2029 | …InYearFour | 177,000,000 | 177,000,000 | 177,000 (scale 3) | 0 |  |
| y5_2030 | …InYearFive | 0 | 0 | — (scale 3) | 0 |  |
| after_2030 | …AfterYearFive | 358,524,000 | 358,524,000 | 358,524 (scale 3) | 0 |  |

Table as rendered in the 10-K (cells joined with |; '$' cells dropped):

```
Principal | Revolving Credit Facility | Unsecured Term Loans | Trust Preferred Securities | Total | Company's Share of Joint Venture Debt
2026 | 555,148 | — | 100,000 | — | 655,148 | 1,080,248
2027 | 879,277 | 640,000 | 1,050,000 | — | 2,569,277 | 1,749,857
2028 | 284,550 | — | — | — | 284,550 | 576,793
2029 | 177,000 | — | — | — | 177,000 | —
2030 | — | — | — | — | — | 840,000
Thereafter | 258,524 | — | — | 100,000 | 358,524 | 1,650,300
Total | 2,154,499 | 640,000 | 1,150,000 | 100,000 | 4,044,499 | 5,897,198
```

Printed total in the table ('Total', ladder column): 4,044,499 (scale 3) = 4,044,499,000; six tagged buckets sum to 4,044,499,000; diff 0.

2027 bucket by XBRL dimension (INFERRED: column meaning taken from the filer's member names, not yet confirmed by a human against the table header):

| kind | member | unsecured bank/notes? | shown | USD |
|---|---|---|---:|---:|
| instrument | MortgageAndOtherLoansPayableMember | False | 879,277 | 879,277,000 |
| instrument | CreditFacility2012Member | True | 640,000 | 640,000,000 |
| instrument | TermLoanMember | True | 1,050,000 | 1,050,000,000 |
| instrument | JuniorSubordinatedDebtMember | False | — | 0 |
| jv_share | RelatedPartyTransactionsByRelatedPartyAxis=CorporateJointVentureMember | None | 1,749,857 | 1,749,857,000 |

Dimensioned ladder facts in the same filing (not in companyfacts totals, shown for the reader): 30

- …InNextTwelveMonths ctx=c-476 [DebtInstrumentAxis=MortgageAndOtherLoansPayableMember; RelatedPartyTransactionsByRelatedPartyAxis=CorporateJointVentureMember] shown=555,148 → 555,148,000
- …InNextTwelveMonths ctx=c-477 [DebtInstrumentAxis=CreditFacility2012Member; RelatedPartyTransactionsByRelatedPartyAxis=CorporateJointVentureMember] shown=— → 0
- …InNextTwelveMonths ctx=c-478 [DebtInstrumentAxis=TermLoanMember; RelatedPartyTransactionsByRelatedPartyAxis=CorporateJointVentureMember] shown=100,000 → 100,000,000
- …InNextTwelveMonths ctx=c-479 [DebtInstrumentAxis=JuniorSubordinatedDebtMember; RelatedPartyTransactionsByRelatedPartyAxis=CorporateJointVentureMember] shown=— → 0
- …InNextTwelveMonths ctx=c-285 [RelatedPartyTransactionsByRelatedPartyAxis=CorporateJointVentureMember] shown=1,080,248 → 1,080,248,000
- …InYearTwo ctx=c-476 [DebtInstrumentAxis=MortgageAndOtherLoansPayableMember; RelatedPartyTransactionsByRelatedPartyAxis=CorporateJointVentureMember] shown=879,277 → 879,277,000
- …InYearTwo ctx=c-477 [DebtInstrumentAxis=CreditFacility2012Member; RelatedPartyTransactionsByRelatedPartyAxis=CorporateJointVentureMember] shown=640,000 → 640,000,000
- …InYearTwo ctx=c-478 [DebtInstrumentAxis=TermLoanMember; RelatedPartyTransactionsByRelatedPartyAxis=CorporateJointVentureMember] shown=1,050,000 → 1,050,000,000
- …InYearTwo ctx=c-479 [DebtInstrumentAxis=JuniorSubordinatedDebtMember; RelatedPartyTransactionsByRelatedPartyAxis=CorporateJointVentureMember] shown=— → 0
- …InYearTwo ctx=c-285 [RelatedPartyTransactionsByRelatedPartyAxis=CorporateJointVentureMember] shown=1,749,857 → 1,749,857,000
- …InYearThree ctx=c-476 [DebtInstrumentAxis=MortgageAndOtherLoansPayableMember; RelatedPartyTransactionsByRelatedPartyAxis=CorporateJointVentureMember] shown=284,550 → 284,550,000
- …InYearThree ctx=c-477 [DebtInstrumentAxis=CreditFacility2012Member; RelatedPartyTransactionsByRelatedPartyAxis=CorporateJointVentureMember] shown=— → 0
- …InYearThree ctx=c-478 [DebtInstrumentAxis=TermLoanMember; RelatedPartyTransactionsByRelatedPartyAxis=CorporateJointVentureMember] shown=— → 0
- …InYearThree ctx=c-479 [DebtInstrumentAxis=JuniorSubordinatedDebtMember; RelatedPartyTransactionsByRelatedPartyAxis=CorporateJointVentureMember] shown=— → 0
- …InYearThree ctx=c-285 [RelatedPartyTransactionsByRelatedPartyAxis=CorporateJointVentureMember] shown=576,793 → 576,793,000
- …InYearFour ctx=c-476 [DebtInstrumentAxis=MortgageAndOtherLoansPayableMember; RelatedPartyTransactionsByRelatedPartyAxis=CorporateJointVentureMember] shown=177,000 → 177,000,000
- …InYearFour ctx=c-477 [DebtInstrumentAxis=CreditFacility2012Member; RelatedPartyTransactionsByRelatedPartyAxis=CorporateJointVentureMember] shown=— → 0
- …InYearFour ctx=c-478 [DebtInstrumentAxis=TermLoanMember; RelatedPartyTransactionsByRelatedPartyAxis=CorporateJointVentureMember] shown=— → 0
- …InYearFour ctx=c-479 [DebtInstrumentAxis=JuniorSubordinatedDebtMember; RelatedPartyTransactionsByRelatedPartyAxis=CorporateJointVentureMember] shown=— → 0
- …InYearFour ctx=c-285 [RelatedPartyTransactionsByRelatedPartyAxis=CorporateJointVentureMember] shown=— → 0
- …InYearFive ctx=c-476 [DebtInstrumentAxis=MortgageAndOtherLoansPayableMember; RelatedPartyTransactionsByRelatedPartyAxis=CorporateJointVentureMember] shown=— → 0
- …InYearFive ctx=c-477 [DebtInstrumentAxis=CreditFacility2012Member; RelatedPartyTransactionsByRelatedPartyAxis=CorporateJointVentureMember] shown=— → 0
- …InYearFive ctx=c-478 [DebtInstrumentAxis=TermLoanMember; RelatedPartyTransactionsByRelatedPartyAxis=CorporateJointVentureMember] shown=— → 0
- …InYearFive ctx=c-479 [DebtInstrumentAxis=JuniorSubordinatedDebtMember; RelatedPartyTransactionsByRelatedPartyAxis=CorporateJointVentureMember] shown=— → 0
- …InYearFive ctx=c-285 [RelatedPartyTransactionsByRelatedPartyAxis=CorporateJointVentureMember] shown=840,000 → 840,000,000
- …AfterYearFive ctx=c-476 [DebtInstrumentAxis=MortgageAndOtherLoansPayableMember; RelatedPartyTransactionsByRelatedPartyAxis=CorporateJointVentureMember] shown=258,524 → 258,524,000
- …AfterYearFive ctx=c-477 [DebtInstrumentAxis=CreditFacility2012Member; RelatedPartyTransactionsByRelatedPartyAxis=CorporateJointVentureMember] shown=— → 0
- …AfterYearFive ctx=c-478 [DebtInstrumentAxis=TermLoanMember; RelatedPartyTransactionsByRelatedPartyAxis=CorporateJointVentureMember] shown=— → 0
- …AfterYearFive ctx=c-479 [DebtInstrumentAxis=JuniorSubordinatedDebtMember; RelatedPartyTransactionsByRelatedPartyAxis=CorporateJointVentureMember] shown=100,000 → 100,000,000
- …AfterYearFive ctx=c-285 [RelatedPartyTransactionsByRelatedPartyAxis=CorporateJointVentureMember] shown=1,650,300 → 1,650,300,000

### Cousins Properties
Source: https://www.sec.gov/Archives/edgar/data/25232/000002523226000014/cuz-20251231.htm

Method: the inline-XBRL facts rendered *inside the 10-K document* (dimensionless context, instant 2025-12-31), displayed number × 10^scale, compared with the companyfacts value.

| bucket | tag | extracted (companyfacts) | 10-K displayed → USD | shown text | diff | note |
|---|---|---:|---:|---|---:|---|
| y1_2026 | …InNextTwelveMonths | 870,127,000 | 870,127,000 | 870,127 (scale 3) | 0 |  |
| y2_2027 | …InYearTwo | 341,000,000 | 341,000,000 | 341,000 (scale 3) | 0 |  |
| y3_2028 | …InYearThree | 250,000,000 | 250,000,000 | 250,000 (scale 3) | 0 |  |
| y4_2029 | …InYearFour | 275,000,000 | 275,000,000 | 275,000 (scale 3) | 0 |  |
| y5_2030 | …InYearFive | 500,000,000 | 500,000,000 | 500,000 (scale 3) | 0 |  |
| after_2030 | …AfterYearFive | 1,121,000,000 | 1,121,000,000 | 1,121,000 (scale 3) | 0 |  |

Table as rendered in the 10-K (cells joined with |; '$' cells dropped):

```
2026 | 870,127
2027 | 341,000
2028 | 250,000
2029 | 275,000
2030 | 500,000
Thereafter | 1,121,000
3,357,127
```

Printed total in the table ('(unlabelled subtotal row)', ladder column): 3,357,127 (scale 3) = 3,357,127,000; six tagged buckets sum to 3,357,127,000; diff 0.

### JBG Smith
Source: https://www.sec.gov/Archives/edgar/data/1689796/000110465926016450/jbgs-20251231x10k.htm

Method: the inline-XBRL facts rendered *inside the 10-K document* (dimensionless context, instant 2025-12-31), displayed number × 10^scale, compared with the companyfacts value.

| bucket | tag | extracted (companyfacts) | 10-K displayed → USD | shown text | diff | note |
|---|---|---:|---:|---|---:|---|
| y1_2026 | …InNextTwelveMonths | 170,820,000 | 170,820,000 | 170,820 (scale 3) | 0 |  |
| y2_2027 | …InYearTwo | 676,303,000 | 676,303,000 | 676,303 (scale 3) | 0 |  |
| y3_2028 | …InYearThree | 610,147,000 | 610,147,000 | 610,147 (scale 3) | 0 |  |
| y4_2029 | …InYearFour | 278,987,000 | 278,987,000 | 278,987 (scale 3) | 0 |  |
| y5_2030 | …InYearFive | 810,332,000 | 810,332,000 | 810,332 (scale 3) | 0 |  |
| after_2030 | …AfterYearFive | n/a | n/a | n/a | n/a | not tagged (dimensionless) in 10-K text |

Table as rendered in the 10-K (cells joined with |; '$' cells dropped):

```
Year ending December 31, | Amount
(In thousands)
2026 | 170,820
2027 | 676,303
2028 | 610,147
2029 | 278,987
2030 | 810,332
Total | 2,546,589
```

Printed total in the table ('Total', ladder column): 2,546,589 (scale 3) = 2,546,589,000; six tagged buckets sum to 2,546,589,000; diff 0.

NOTE: bucket(s) after_2030 are not tagged, and the filer's own printed total equals the sum of the tagged buckets. So in the filer's table the missing bucket(s) add nothing, and the upper-bound 2027 share equals the printed-table share. The data stays missing (no imputation) and the scoring is unchanged.

### Piedmont Office
Source: https://www.sec.gov/Archives/edgar/data/1042776/000104277626000012/pdm-20251231.htm

Method: the inline-XBRL facts rendered *inside the 10-K document* (dimensionless context, instant 2025-12-31), displayed number × 10^scale, compared with the companyfacts value.

| bucket | tag | extracted (companyfacts) | 10-K displayed → USD | shown text | diff | note |
|---|---|---:|---:|---|---:|---|
| y1_2026 | …InNextTwelveMonths | 3,433,000 | 3,433,000 | 3,433 (scale 3) | 0 |  |
| y2_2027 | …InYearTwo | 328,894,000 | 328,894,000 | 328,894 (scale 3) | 0 |  |
| y3_2028 | …InYearThree | 515,753,000 | 515,753,000 | 515,753 (scale 3) | 0 |  |
| y4_2029 | …InYearFour | 400,000,000 | 400,000,000 | 400,000 (scale 3) | 0 |  |
| y5_2030 | …InYearFive | 300,000,000 | 300,000,000 | 300,000 (scale 3) | 0 |  |
| after_2030 | …AfterYearFive | 700,000,000 | 700,000,000 | 700,000 (scale 3) | 0 |  |

Table as rendered in the 10-K (cells joined with |; '$' cells dropped):

```
2026 | 3,433
2027 | 328,894
2028 | 515,753
2029 | 400,000
2030 | 300,000
Thereafter | 700,000
Total | 2,248,080
```

Printed total in the table ('Total', ladder column): 2,248,080 (scale 3) = 2,248,080,000; six tagged buckets sum to 2,248,080,000; diff 0.

### Office Properties Income Trust
Source: https://www.sec.gov/Archives/edgar/data/1456772/000145677226000022/opi-20251231.htm

Method: the inline-XBRL facts rendered *inside the 10-K document* (dimensionless context, instant 2025-12-31), displayed number × 10^scale, compared with the companyfacts value.

| bucket | tag | extracted (companyfacts) | 10-K displayed → USD | shown text | diff | note |
|---|---|---:|---:|---|---:|---|
| y1_2026 | …InNextTwelveMonths | 144,154,000 | 144,154,000 | 144,154 (scale 3) | 0 |  |
| y2_2027 | …InYearTwo | 921,300,000 | 921,300,000 | 921,300 (scale 3) | 0 |  |
| y3_2028 | …InYearThree | 123,487,000 | 123,487,000 | 123,487 (scale 3) | 0 |  |
| y4_2029 | …InYearFour | 910,278,000 | 910,278,000 | 910,278 (scale 3) | 0 |  |
| y5_2030 | …InYearFive | 14,739,000 | 14,739,000 | 14,739 (scale 3) | 0 |  |
| after_2030 | …AfterYearFive | 317,656,000 | 317,656,000 | 317,656 (scale 3) | 0 |  |

Table as rendered in the 10-K (cells joined with |; '$' cells dropped):

```
Year | Principal Payment
2026 | 144,154
2027 | 921,300
2028 | 123,487
2029 | 910,278
2030 | 14,739
Thereafter | 317,656
Total (1) | 2,431,614
```

Printed total in the table ('Total (1)', ladder column): 2,431,614 (scale 3) = 2,431,614,000; six tagged buckets sum to 2,431,614,000; diff 0.

### Empire State Realty Trust
Source: https://www.sec.gov/Archives/edgar/data/1541401/000154140126000008/esrt-20251231.htm

Method: the inline-XBRL facts rendered *inside the 10-K document* (dimensionless context, instant 2025-12-31), displayed number × 10^scale, compared with the companyfacts value.

| bucket | tag | extracted (companyfacts) | 10-K displayed → USD | shown text | diff | note |
|---|---|---:|---:|---|---:|---|
| y1_2026 | …InNextTwelveMonths | 53,958,000 | 53,958,000 | 53,958 (scale 3) | 0 |  |
| y2_2027 | …InYearTwo | 159,276,000 | 159,276,000 | 159,276 (scale 3) | 0 |  |
| y3_2028 | …InYearThree | 149,646,000 | 149,646,000 | 149,646 (scale 3) | 0 |  |
| y4_2029 | …InYearFour | 398,890,000 | 398,890,000 | 398,890 (scale 3) | 0 |  |
| y5_2030 | …InYearFive | 513,111,000 | 513,111,000 | 513,111 (scale 3) | 0 |  |
| after_2030 | …AfterYearFive | 1,114,130,000 | 1,114,130,000 | 1,114,130 (scale 3) | 0 |  |

Table as rendered in the 10-K (cells joined with |; '$' cells dropped):

```
Year | Amortization | Maturities | Total
2026 | 3,958 | 50,000 | 53,958
2027 | 4,276 | 155,000 | 159,276
2028 | 3,555 | 146,091 | 149,646
2029 | 3,890 | 395,000 | 398,890
2030 | 4,511 | 508,600 | 513,111
Thereafter | 10,123 | 1,104,007 | 1,114,130
Total | 30,313 | 2,358,698 | 2,389,011
```

Printed total in the table ('Total', ladder column): 2,389,011 (scale 3) = 2,389,011,000; six tagged buckets sum to 2,389,011,000; diff 0.

### BXP
NOT DONE: n/a: no ladder tags at 2025-12-31 in companyfacts, so there is nothing to compare (no 10-K table was parsed or guessed)

### CBL & Associates
Source: https://www.sec.gov/Archives/edgar/data/910612/000119312526087049/cbl-20251231.htm

Method: the inline-XBRL facts rendered *inside the 10-K document* (dimensionless context, instant 2025-12-31), displayed number × 10^scale, compared with the companyfacts value.

| bucket | tag | extracted (companyfacts) | 10-K displayed → USD | shown text | diff | note |
|---|---|---:|---:|---|---:|---|
| y1_2026 | …InNextTwelveMonths | 1,281,692,000 | 1,281,692,000 | 1,281,692 (scale 3) | 0 |  |
| y2_2027 | …InYearTwo | 11,195 | 11,195 | 11,195 (scale 0) | 0 | SCALE MISMATCH: tagged scale 0 while the other ladder cells in this table use scale 3; if read at the table's scale the value would be 11,195,000. Value NOT changed (filer's tag kept). |
| y3_2028 | …InYearThree | 134,781,000 | 134,781,000 | 134,781 (scale 3) | 0 |  |
| y4_2029 | …InYearFour | 7,939,000 | 7,939,000 | 7,939 (scale 3) | 0 |  |
| y5_2030 | …InYearFive | 740,144,000 | 740,144,000 | 740,144 (scale 3) | 0 |  |
| after_2030 | …AfterYearFive | 59,831,000 | 59,831,000 | 59,831 (scale 3) | 0 |  |

Table as rendered in the 10-K (cells joined with |; '$' cells dropped):

```
2026 | 1,281,692
2027 | 11,195
2028 | 134,781
2029 | 7,939
2030 | 740,144
Thereafter | 59,831
Total | 2,235,582
Principal balance of a loan with a maturity date prior to December 31, 2025 (1) | 19,438
Total mortgage and other indebtedness | 2,255,020
```

Printed total in the table ('Total', ladder column): 2,235,582 (scale 3) = 2,235,582,000; six tagged buckets sum to 2,224,398,195; diff -11,183,805.

Dimensioned ladder facts in the same filing (not in companyfacts totals, shown for the reader): 2

- …InNextTwelveMonths ctx=C_f505c324-6b9e-43b5-aaf9-f4dcc9c54532 [DebtInstrumentAxis=LoansSecuredByThreePropertiesAndSecuredTermLoanMember] shown=624,083 → 624,083,000
- …InNextTwelveMonths ctx=C_61b76345-5ed9-42e1-adab-8261f785d419 [LongtermDebtTypeAxis=SecuredTermLoanMember] shown=646,722 → 646,722,000

### Simon Property Group
Source: https://www.sec.gov/Archives/edgar/data/1063761/000110465926019419/spg-20251231x10k.htm

Method: the inline-XBRL facts rendered *inside the 10-K document* (dimensionless context, instant 2025-12-31), displayed number × 10^scale, compared with the companyfacts value.

| bucket | tag | extracted (companyfacts) | 10-K displayed → USD | shown text | diff | note |
|---|---|---:|---:|---|---:|---|
| y1_2026 | …InNextTwelveMonths | 5,905,606,000 | 5,905,606,000 | 5,905,606 (scale 3) | 0 |  |
| y2_2027 | …InYearTwo | 3,936,773,000 | 3,936,773,000 | 3,936,773 (scale 3) | 0 |  |
| y3_2028 | …InYearThree | 2,296,651,000 | 2,296,651,000 | 2,296,651 (scale 3) | 0 |  |
| y4_2029 | …InYearFour | 2,940,031,000 | 2,940,031,000 | 2,940,031 (scale 3) | 0 |  |
| y5_2030 | …InYearFive | 1,657,864,000 | 1,657,864,000 | 1,657,864 (scale 3) | 0 |  |
| after_2030 | …AfterYearFive | 11,858,614,000 | 11,858,614,000 | 11,858,614 (scale 3) | 0 |  |

Table as rendered in the 10-K (cells joined with |; '$' cells dropped):

```
2026 | 5,905,606
2027 | 3,936,773
2028 | 2,296,651
2029 | 2,940,031
2030 | 1,657,864
Thereafter | 11,858,614
Total principal maturities | 28,595,539
Net unamortized debt premium | 1,065
Net unamortized debt discount | (73,175)
Debt issuance costs, net | (117,853)
Other Debt Obligations and Other | 24,599
Total mortgages and unsecured indebtedness | 28,430,175
```

Printed total in the table ('Total principal maturities', ladder column): 28,595,539 (scale 3) = 28,595,539,000; six tagged buckets sum to 28,595,539,000; diff 0.

2027 bucket by XBRL dimension (INFERRED: column meaning taken from the filer's member names, not yet confirmed by a human against the table header):

| kind | member | unsecured bank/notes? | shown | USD |
|---|---|---|---:|---:|
| jv_share | EquityMethodInvestmentNonconsolidatedInvesteeAxis=EquityMethodInvesteesExcludingThoseSpecifiedMember; RealEstatePropertiesAxis=UnconsolidatedPropertiesMember | None | 2,459,508 | 2,459,508,000 |

Dimensioned ladder facts in the same filing (not in companyfacts totals, shown for the reader): 6

- …InNextTwelveMonths ctx=As_Of_12_31_2025_us-gaap_EquityMethodInvestmentNonconsolidatedInvesteeAxis_spg_EquityMethodInvesteesExcludingThoseSpecifiedMember_us-gaap_RealEstatePropertiesAxis_us-gaap_UnconsolidatedPropertiesMember_GK06KjSvZ0Srv67_dq3DsA [EquityMethodInvestmentNonconsolidatedInvesteeAxis=EquityMethodInvesteesExcludingThoseSpecifiedMember; RealEstatePropertiesAxis=UnconsolidatedPropertiesMember] shown=3,573,638 → 3,573,638,000
- …InYearTwo ctx=As_Of_12_31_2025_us-gaap_EquityMethodInvestmentNonconsolidatedInvesteeAxis_spg_EquityMethodInvesteesExcludingThoseSpecifiedMember_us-gaap_RealEstatePropertiesAxis_us-gaap_UnconsolidatedPropertiesMember_GK06KjSvZ0Srv67_dq3DsA [EquityMethodInvestmentNonconsolidatedInvesteeAxis=EquityMethodInvesteesExcludingThoseSpecifiedMember; RealEstatePropertiesAxis=UnconsolidatedPropertiesMember] shown=2,459,508 → 2,459,508,000
- …InYearThree ctx=As_Of_12_31_2025_us-gaap_EquityMethodInvestmentNonconsolidatedInvesteeAxis_spg_EquityMethodInvesteesExcludingThoseSpecifiedMember_us-gaap_RealEstatePropertiesAxis_us-gaap_UnconsolidatedPropertiesMember_GK06KjSvZ0Srv67_dq3DsA [EquityMethodInvestmentNonconsolidatedInvesteeAxis=EquityMethodInvesteesExcludingThoseSpecifiedMember; RealEstatePropertiesAxis=UnconsolidatedPropertiesMember] shown=3,175,273 → 3,175,273,000
- …InYearFour ctx=As_Of_12_31_2025_us-gaap_EquityMethodInvestmentNonconsolidatedInvesteeAxis_spg_EquityMethodInvesteesExcludingThoseSpecifiedMember_us-gaap_RealEstatePropertiesAxis_us-gaap_UnconsolidatedPropertiesMember_GK06KjSvZ0Srv67_dq3DsA [EquityMethodInvestmentNonconsolidatedInvesteeAxis=EquityMethodInvesteesExcludingThoseSpecifiedMember; RealEstatePropertiesAxis=UnconsolidatedPropertiesMember] shown=749,397 → 749,397,000
- …InYearFive ctx=As_Of_12_31_2025_us-gaap_EquityMethodInvestmentNonconsolidatedInvesteeAxis_spg_EquityMethodInvesteesExcludingThoseSpecifiedMember_us-gaap_RealEstatePropertiesAxis_us-gaap_UnconsolidatedPropertiesMember_GK06KjSvZ0Srv67_dq3DsA [EquityMethodInvestmentNonconsolidatedInvesteeAxis=EquityMethodInvesteesExcludingThoseSpecifiedMember; RealEstatePropertiesAxis=UnconsolidatedPropertiesMember] shown=2,113,931 → 2,113,931,000
- …AfterYearFive ctx=As_Of_12_31_2025_us-gaap_EquityMethodInvestmentNonconsolidatedInvesteeAxis_spg_EquityMethodInvesteesExcludingThoseSpecifiedMember_us-gaap_RealEstatePropertiesAxis_us-gaap_UnconsolidatedPropertiesMember_GK06KjSvZ0Srv67_dq3DsA [EquityMethodInvestmentNonconsolidatedInvesteeAxis=EquityMethodInvesteesExcludingThoseSpecifiedMember; RealEstatePropertiesAxis=UnconsolidatedPropertiesMember] shown=4,344,553 → 4,344,553,000

### Brixmor
Source: https://www.sec.gov/Archives/edgar/data/1581068/000158106826000007/brx-20251231.htm

Method: the inline-XBRL facts rendered *inside the 10-K document* (dimensionless context, instant 2025-12-31), displayed number × 10^scale, compared with the companyfacts value.

| bucket | tag | extracted (companyfacts) | 10-K displayed → USD | shown text | diff | note |
|---|---|---:|---:|---|---:|---|
| y1_2026 | …InNextTwelveMonths | 607,542,000 | 607,542,000 | 607,542 (scale 3) | 0 |  |
| y2_2027 | …InYearTwo | 400,000,000 | 400,000,000 | 400,000 (scale 3) | 0 |  |
| y3_2028 | …InYearThree | 357,708,000 | 357,708,000 | 357,708 (scale 3) | 0 |  |
| y4_2029 | …InYearFour | 753,203,000 | 753,203,000 | 753,203 (scale 3) | 0 |  |
| y5_2030 | …InYearFive | 1,300,000,000 | 1,300,000,000 | 1,300,000 (scale 3) | 0 |  |
| after_2030 | …AfterYearFive | 2,100,000,000 | 2,100,000,000 | 2,100,000 (scale 3) | 0 |  |

Table as rendered in the 10-K (cells joined with |; '$' cells dropped):

```
Year ending December 31,
2026 | 607,542
2027 | 400,000
2028 | 357,708
2029 | 753,203
2030 | 1,300,000
Thereafter | 2,100,000
Total debt maturities | 5,518,453
Net unamortized premium | 10,277
Net unamortized debt issuance costs | (33,977)
Total debt obligations, net | 5,494,753
```

Printed total in the table ('Total debt maturities', ladder column): 5,518,453 (scale 3) = 5,518,453,000; six tagged buckets sum to 5,518,453,000; diff 0.

### Acadia Realty
Source: https://www.sec.gov/Archives/edgar/data/899629/000119312526051677/akr-20251231.htm

Method: the inline-XBRL facts rendered *inside the 10-K document* (dimensionless context, instant 2025-12-31), displayed number × 10^scale, compared with the companyfacts value.

| bucket | tag | extracted (companyfacts) | 10-K displayed → USD | shown text | diff | note |
|---|---|---:|---:|---|---:|---|
| y1_2026 | …InNextTwelveMonths | 292,287,000 | 292,287,000 | 292,287 (scale 3) | 0 |  |
| y2_2027 | …InYearTwo | 309,638,000 | 309,638,000 | 309,638 (scale 3) | 0 |  |
| y3_2028 | …InYearThree | 845,235,000 | 845,235,000 | 845,235 (scale 3) | 0 |  |
| y4_2029 | …InYearFour | 98,292,000 | 98,292,000 | 98,292 (scale 3) | 0 |  |
| y5_2030 | …InYearFive | 326,850,000 | 326,850,000 | 326,850 (scale 3) | 0 |  |
| after_2030 | …AfterYearFive | 1,065,000 | 1,065,000 | 1,065 (scale 3) | 0 |  |

Table as rendered in the 10-K (cells joined with |; '$' cells dropped):

```
Year Ending December 31, | Principal Repayments
2026 | 292,287
2027 | 309,638
2028 | 845,235
2029 | 98,292
2030 | 326,850
Thereafter | 1,065
1,873,367
Unamortized premium | 926
Net unamortized debt issuance costs | (11,387 | )
Total indebtedness | 1,862,906
```

Printed total in the table ('(unlabelled subtotal row)', ladder column): 1,873,367 (scale 3) = 1,873,367,000; six tagged buckets sum to 1,873,367,000; diff 0.

2027 bucket by XBRL dimension (INFERRED: column meaning taken from the filer's member names, not yet confirmed by a human against the table header):

| kind | member | unsecured bank/notes? | shown | USD |
|---|---|---|---:|---:|
| instrument | DebtWithExtensionOptionsMember | False | 252.4 | 252,400,000 |

Dimensioned ladder facts in the same filing (not in companyfacts totals, shown for the reader): 3

- …InNextTwelveMonths ctx=C_1e96ff32-5e77-4538-aa9e-2edfdda6e69c [DebtInstrumentAxis=DebtWithExtensionOptionsMember] shown=188.0 → 188,000,000
- …InYearTwo ctx=C_1e96ff32-5e77-4538-aa9e-2edfdda6e69c [DebtInstrumentAxis=DebtWithExtensionOptionsMember] shown=252.4 → 252,400,000
- …InYearThree ctx=C_1e96ff32-5e77-4538-aa9e-2edfdda6e69c [DebtInstrumentAxis=DebtWithExtensionOptionsMember] shown=682.0 → 682,000,000

### Kite Realty
Source: https://www.sec.gov/Archives/edgar/data/1286043/000128604326000009/krg-20251231.htm

Method: the inline-XBRL facts rendered *inside the 10-K document* (dimensionless context, instant 2025-12-31), displayed number × 10^scale, compared with the companyfacts value.

| bucket | tag | extracted (companyfacts) | 10-K displayed → USD | shown text | diff | note |
|---|---|---:|---:|---|---:|---|
| y1_2026 | …InNextTwelveMonths | 415,181,000 | 415,181,000 | 415,181 (scale 3) | 0 |  |
| y2_2027 | …InYearTwo | 522,568,000 | 522,568,000 | 522,568 (scale 3) | 0 |  |
| y3_2028 | …InYearThree | 187,943,000 | 187,943,000 | 187,943 (scale 3) | 0 |  |
| y4_2029 | …InYearFour | 403,474,000 | 403,474,000 | 403,474 (scale 3) | 0 |  |
| y5_2030 | …InYearFive | 403,036,000 | 403,036,000 | 403,036 (scale 3) | 0 |  |
| after_2030 | …AfterYearFive | 1,095,735,000 | 1,095,735,000 | 1,095,735 (scale 3) | 0 |  |

Table as rendered in the 10-K (cells joined with |; '$' cells dropped):

```
Secured Debt
Scheduled Principal Payments | Term Maturities | Unsecured Debt | Total
2026 | 4,581 | 10,600 | 400,000 | 415,181
2027 | 2,662 | 19,906 | 500,000 | 522,568
2028 | 2,943 | — | 185,000 | 187,943
2029 | 3,474 | — | 400,000 | 403,474
2030 | 2,936 | 100 | 400,000 | 403,036
Thereafter | 3,186 | 92,549 | 1,000,000 | 1,095,735
19,782 | 123,155 | 2,885,000 | 3,027,937
Debt discounts, premiums and issuance costs, net | (2,459)
Mortgage and other indebtedness, net | 3,025,478
```

Printed total in the table ('(unlabelled subtotal row)', ladder column): 3,027,937 (scale 3) = 3,027,937,000; six tagged buckets sum to 3,027,937,000; diff 0.

### Vornado Realty Trust
NOT DONE: n/a: no ladder tags at 2025-12-31 in companyfacts, so there is nothing to compare (no 10-K table was parsed or guessed)

### Kilroy Realty
Source: https://www.sec.gov/Archives/edgar/data/1025996/000162828026007051/krc-20251231.htm

Method: the inline-XBRL facts rendered *inside the 10-K document* (dimensionless context, instant 2025-12-31), displayed number × 10^scale, compared with the companyfacts value.

| bucket | tag | extracted (companyfacts) | 10-K displayed → USD | shown text | diff | note |
|---|---|---:|---:|---|---:|---|
| y1_2026 | …InNextTwelveMonths | 601,317,000 | 601,317,000 | 601,317 (scale 3) | 0 |  |
| y2_2027 | …InYearTwo | 249,125,000 | 249,125,000 | 249,125 (scale 3) | 0 |  |
| y3_2028 | …InYearThree | n/a | n/a | n/a | n/a | not tagged (dimensionless) in 10-K text |
| y4_2029 | …InYearFour | n/a | n/a | n/a | n/a | not tagged (dimensionless) in 10-K text |
| y5_2030 | …InYearFive | n/a | n/a | n/a | n/a | not tagged (dimensionless) in 10-K text |
| after_2030 | …AfterYearFive | 2,400,000,000 | 2,400,000,000 | 2,400,000 (scale 3) | 0 |  |

Table as rendered in the 10-K (cells joined with |; '$' cells dropped):

```
Year | (in thousands)
2026 | 601,317
2027 | 249,125
2028 | 400,000
2029 | 475,000
2030 | 500,000
Thereafter | 2,400,000
Total aggregate principal value | 4,625,442
Less: unamortized net discounts and deferred financing costs (1) | (35,983)
Total debt, net | 4,589,459
```

Printed total in the table ('Total aggregate principal value', ladder column): 4,625,442 (scale 3) = 4,625,442,000; six tagged buckets sum to 3,250,442,000; diff -1,375,000,000.

Dimensioned ladder facts in the same filing (not in companyfacts totals, shown for the reader): 3

- …InYearThree ctx=c-47 [LegalEntityAxis=KilroyRealtyL.P.Member] shown=400,000 → 400,000,000
- …InYearFour ctx=c-47 [LegalEntityAxis=KilroyRealtyL.P.Member] shown=475,000 → 475,000,000
- …InYearFive ctx=c-47 [LegalEntityAxis=KilroyRealtyL.P.Member] shown=500,000 → 500,000,000

### Highwoods Properties
Source: https://www.sec.gov/Archives/edgar/data/921082/000092108226000005/hiw-20251231.htm

Method: the inline-XBRL facts rendered *inside the 10-K document* (dimensionless context, instant 2025-12-31), displayed number × 10^scale, compared with the companyfacts value.

| bucket | tag | extracted (companyfacts) | 10-K displayed → USD | shown text | diff | note |
|---|---|---:|---:|---|---:|---|
| y1_2026 | …InNextTwelveMonths | 6,682,000 | 6,682,000 | 6,682 (scale 3) | 0 |  |
| y2_2027 | …InYearTwo | 458,736,000 | 458,736,000 | 458,736 (scale 3) | 0 |  |
| y3_2028 | …InYearThree | 723,928,000 | 723,928,000 | 723,928 (scale 3) | 0 |  |
| y4_2029 | …InYearFour | 717,027,000 | 717,027,000 | 717,027 (scale 3) | 0 |  |
| y5_2030 | …InYearFive | 404,662,000 | 404,662,000 | 404,662 (scale 3) | 0 |  |
| after_2030 | …AfterYearFive | 1,259,119,000 | 1,259,119,000 | 1,259,119 (scale 3) | 0 |  |

Table as rendered in the 10-K (cells joined with |; '$' cells dropped):

```
Years Ending December 31, | Amount
2026 | 6,682
2027 | 458,736
2028 | 723,928
2029 | 717,027
2030 | 404,662
Thereafter | 1,259,119
Less-unamortized debt issuance costs | (15,976)
3,554,178
```

Printed total: NOT FOUND. The row directly below the year rows is neither labelled 'Total' nor an unlabelled subtotal with a number in the ladder column. Not guessed.

### Douglas Emmett
NOT DONE: n/a: no ladder tags at 2025-12-31 in companyfacts, so there is nothing to compare (no 10-K table was parsed or guessed)

### Hudson Pacific Properties
NOT DONE: n/a: no ladder tags at 2025-12-31 in companyfacts, so there is nothing to compare (no 10-K table was parsed or guessed)

### Brandywine Realty Trust
Source: https://www.sec.gov/Archives/edgar/data/790816/000079081626000008/bdn-20251231.htm

Method: the inline-XBRL facts rendered *inside the 10-K document* (dimensionless context, instant 2025-12-31), displayed number × 10^scale, compared with the companyfacts value.

| bucket | tag | extracted (companyfacts) | 10-K displayed → USD | shown text | diff | note |
|---|---|---:|---:|---|---:|---|
| y1_2026 | …InNextTwelveMonths | 178,014,000 | 178,014,000 | 178,014 (scale 3) | 0 |  |
| y2_2027 | …InYearTwo | 700,000,000 | 700,000,000 | 700,000 (scale 3) | 0 |  |
| y3_2028 | …InYearThree | 350,000,000 | 350,000,000 | 350,000 (scale 3) | 0 |  |
| y4_2029 | …InYearFour | 900,000,000 | 900,000,000 | 900,000 (scale 3) | 0 |  |
| y5_2030 | …InYearFive | 0 | 0 | — (scale 3) | 0 |  |
| after_2030 | …AfterYearFive | 435,934,000 | 435,934,000 | 435,934 (scale 3) | 0 |  |

Table as rendered in the 10-K (cells joined with |; '$' cells dropped):

```
2026 | 178,014
2027 | 700,000
2028 | 350,000
2029 | 900,000
2030 | —
Thereafter | 435,934
Total principal payments | 2,563,948
Net unamortized premiums/(discounts) | 7,760
Net deferred financing costs | (14,846)
Outstanding indebtedness | 2,556,862
```

Printed total in the table ('Total principal payments', ladder column): 2,563,948 (scale 3) = 2,563,948,000; six tagged buckets sum to 2,563,948,000; diff 0.

2027 bucket by XBRL dimension (INFERRED: column meaning taken from the filer's member names, not yet confirmed by a human against the table header):

| kind | member | unsecured bank/notes? | shown | USD |
|---|---|---|---:|---:|
| jv_share | ScheduleOfEquityMethodInvestmentEquityMethodInvesteeNameAxis=UnconsolidatedRealEstateVenturesMember | None | 155,344 | 155,344,000 |

Dimensioned ladder facts in the same filing (not in companyfacts totals, shown for the reader): 6

- …InNextTwelveMonths ctx=c-382 [ScheduleOfEquityMethodInvestmentEquityMethodInvesteeNameAxis=UnconsolidatedRealEstateVenturesMember] shown=— → 0
- …InYearTwo ctx=c-382 [ScheduleOfEquityMethodInvestmentEquityMethodInvesteeNameAxis=UnconsolidatedRealEstateVenturesMember] shown=155,344 → 155,344,000
- …InYearThree ctx=c-382 [ScheduleOfEquityMethodInvestmentEquityMethodInvesteeNameAxis=UnconsolidatedRealEstateVenturesMember] shown=220,000 → 220,000,000
- …InYearFour ctx=c-382 [ScheduleOfEquityMethodInvestmentEquityMethodInvesteeNameAxis=UnconsolidatedRealEstateVenturesMember] shown=211,097 → 211,097,000
- …InYearFive ctx=c-382 [ScheduleOfEquityMethodInvestmentEquityMethodInvesteeNameAxis=UnconsolidatedRealEstateVenturesMember] shown=— → 0
- …AfterYearFive ctx=c-382 [ScheduleOfEquityMethodInvestmentEquityMethodInvesteeNameAxis=UnconsolidatedRealEstateVenturesMember] shown=— → 0

### Regency Centers
Source: https://www.sec.gov/Archives/edgar/data/910606/000119312526051668/reg-20251231.htm

Method: the inline-XBRL facts rendered *inside the 10-K document* (dimensionless context, instant 2025-12-31), displayed number × 10^scale, compared with the companyfacts value.

| bucket | tag | extracted (companyfacts) | 10-K displayed → USD | shown text | diff | note |
|---|---|---:|---:|---|---:|---|
| y1_2026 | …InNextTwelveMonths | 360,684,000 | 360,684,000 | 360,684 (scale 3) | 0 |  |
| y2_2027 | …InYearTwo | 757,609,000 | 757,609,000 | 757,609 (scale 3) | 0 |  |
| y3_2028 | …InYearThree | 480,304,000 | 480,304,000 | 480,304 (scale 3) | 0 |  |
| y4_2029 | …InYearFour | 527,739,000 | 527,739,000 | 527,739 (scale 3) | 0 |  |
| y5_2030 | …InYearFive | 607,608,000 | 607,608,000 | 607,608 (scale 3) | 0 |  |
| after_2030 | …AfterYearFive | 2,064,887,000 | 2,064,887,000 | 2,064,887 (scale 3) | 0 |  |

Table as rendered in the 10-K (cells joined with |; '$' cells dropped):

```
(in thousands) | December 31, 2025
Scheduled Principal Payments and Maturities by Year: | Scheduled Principal Payments | Mortgage Loan Maturities | Unsecured Maturities (1) | Total
2026 | 12,836 | 147,848 | 200,000 | 360,684
2027 | 10,051 | 222,558 | 525,000 | 757,609
2028 | 8,365 | 51,939 | 420,000 | 480,304
2029 | 5,619 | 97,120 | 425,000 | 527,739
2030 | 5,445 | 2,163 | 600,000 | 607,608
Beyond 5 Years | 24,210 | 190,677 | 1,850,000 | 2,064,887
Unamortized debt premium/(discount) and issuance costs | — | (32,394 | ) | (27,136 | ) | (59,530 | )
Total | 66,526 | 679,911 | 3,992,864 | 4,739,301
```

Printed total: NOT FOUND. The row directly below the year rows is neither labelled 'Total' nor an unlabelled subtotal with a number in the ladder column. Not guessed.

2027 bucket by XBRL dimension (INFERRED: column meaning taken from the filer's member names, not yet confirmed by a human against the table header):

| kind | member | unsecured bank/notes? | shown | USD |
|---|---|---|---:|---:|
| instrument | MortgagesMember | False | 7,303 | 7,303,000 |
| instrument | MortgagesMember | False | 32,800 | 32,800,000 |
| instrument | UnsecuredDebtMember | True | — | 0 |
| jv_share | LegalEntityAxis=UnconsolidatedInvestmentsinPartnershipMember | None | 40,103 | 40,103,000 |
| jv_share | LegalEntityAxis=UnconsolidatedInvestmentsinPartnershipProRataShareMemberMember | None | 13,417 | 13,417,000 |
| instrument | MortgagesMember | False | 10,051 | 10,051,000 |
| instrument | MortgagesMember | False | 222,558 | 222,558,000 |
| instrument | UnsecuredMaturitiesMember | True | 525,000 | 525,000,000 |

Dimensioned ladder facts in the same filing (not in companyfacts totals, shown for the reader): 48

- …InNextTwelveMonths ctx=C_3070f302-beaf-4288-8fda-553462736cb6 [LegalEntityAxis=UnconsolidatedInvestmentsinPartnershipMember; LongtermDebtTypeAxis=MortgagesMember; ScheduledPrincipalPaymentsAndMaturitiesAxis=ScheduledPrincipalPaymentsMember] shown=7,131 → 7,131,000
- …InNextTwelveMonths ctx=C_e87b8439-8bfa-4403-92d5-03ff6677297a [LongtermDebtTypeAxis=MortgagesMember; LegalEntityAxis=UnconsolidatedInvestmentsinPartnershipMember; ScheduledPrincipalPaymentsAndMaturitiesAxis=MortgageLoanMaturitiesMember] shown=265,346 → 265,346,000
- …InNextTwelveMonths ctx=C_5fae9eb1-f2d4-4a99-a50a-35fd8bd99cd6 [LongtermDebtTypeAxis=UnsecuredDebtMember; ScheduledPrincipalPaymentsAndMaturitiesAxis=UnsecuredMaturitiesMember; LegalEntityAxis=UnconsolidatedInvestmentsinPartnershipMember] shown=20,000 → 20,000,000
- …InNextTwelveMonths ctx=C_11480f13-b944-49b7-8e9d-1578b92c43f5 [LegalEntityAxis=UnconsolidatedInvestmentsinPartnershipMember] shown=292,477 → 292,477,000
- …InNextTwelveMonths ctx=C_731fe8d0-f215-468c-a36d-1b69136cf186 [LegalEntityAxis=UnconsolidatedInvestmentsinPartnershipProRataShareMemberMember] shown=95,689 → 95,689,000
- …InYearTwo ctx=C_3070f302-beaf-4288-8fda-553462736cb6 [LegalEntityAxis=UnconsolidatedInvestmentsinPartnershipMember; LongtermDebtTypeAxis=MortgagesMember; ScheduledPrincipalPaymentsAndMaturitiesAxis=ScheduledPrincipalPaymentsMember] shown=7,303 → 7,303,000
- …InYearTwo ctx=C_e87b8439-8bfa-4403-92d5-03ff6677297a [LongtermDebtTypeAxis=MortgagesMember; LegalEntityAxis=UnconsolidatedInvestmentsinPartnershipMember; ScheduledPrincipalPaymentsAndMaturitiesAxis=MortgageLoanMaturitiesMember] shown=32,800 → 32,800,000
- …InYearTwo ctx=C_5fae9eb1-f2d4-4a99-a50a-35fd8bd99cd6 [LongtermDebtTypeAxis=UnsecuredDebtMember; ScheduledPrincipalPaymentsAndMaturitiesAxis=UnsecuredMaturitiesMember; LegalEntityAxis=UnconsolidatedInvestmentsinPartnershipMember] shown=— → 0
- …InYearTwo ctx=C_11480f13-b944-49b7-8e9d-1578b92c43f5 [LegalEntityAxis=UnconsolidatedInvestmentsinPartnershipMember] shown=40,103 → 40,103,000
- …InYearTwo ctx=C_731fe8d0-f215-468c-a36d-1b69136cf186 [LegalEntityAxis=UnconsolidatedInvestmentsinPartnershipProRataShareMemberMember] shown=13,417 → 13,417,000
- …InYearThree ctx=C_3070f302-beaf-4288-8fda-553462736cb6 [LegalEntityAxis=UnconsolidatedInvestmentsinPartnershipMember; LongtermDebtTypeAxis=MortgagesMember; ScheduledPrincipalPaymentsAndMaturitiesAxis=ScheduledPrincipalPaymentsMember] shown=4,097 → 4,097,000
- …InYearThree ctx=C_e87b8439-8bfa-4403-92d5-03ff6677297a [LongtermDebtTypeAxis=MortgagesMember; LegalEntityAxis=UnconsolidatedInvestmentsinPartnershipMember; ScheduledPrincipalPaymentsAndMaturitiesAxis=MortgageLoanMaturitiesMember] shown=231,235 → 231,235,000
- …InYearThree ctx=C_5fae9eb1-f2d4-4a99-a50a-35fd8bd99cd6 [LongtermDebtTypeAxis=UnsecuredDebtMember; ScheduledPrincipalPaymentsAndMaturitiesAxis=UnsecuredMaturitiesMember; LegalEntityAxis=UnconsolidatedInvestmentsinPartnershipMember] shown=— → 0
- …InYearThree ctx=C_11480f13-b944-49b7-8e9d-1578b92c43f5 [LegalEntityAxis=UnconsolidatedInvestmentsinPartnershipMember] shown=235,332 → 235,332,000
- …InYearThree ctx=C_731fe8d0-f215-468c-a36d-1b69136cf186 [LegalEntityAxis=UnconsolidatedInvestmentsinPartnershipProRataShareMemberMember] shown=81,592 → 81,592,000
- …InYearFour ctx=C_3070f302-beaf-4288-8fda-553462736cb6 [LegalEntityAxis=UnconsolidatedInvestmentsinPartnershipMember; LongtermDebtTypeAxis=MortgagesMember; ScheduledPrincipalPaymentsAndMaturitiesAxis=ScheduledPrincipalPaymentsMember] shown=2,855 → 2,855,000
- …InYearFour ctx=C_e87b8439-8bfa-4403-92d5-03ff6677297a [LongtermDebtTypeAxis=MortgagesMember; LegalEntityAxis=UnconsolidatedInvestmentsinPartnershipMember; ScheduledPrincipalPaymentsAndMaturitiesAxis=MortgageLoanMaturitiesMember] shown=104,434 → 104,434,000
- …InYearFour ctx=C_5fae9eb1-f2d4-4a99-a50a-35fd8bd99cd6 [LongtermDebtTypeAxis=UnsecuredDebtMember; ScheduledPrincipalPaymentsAndMaturitiesAxis=UnsecuredMaturitiesMember; LegalEntityAxis=UnconsolidatedInvestmentsinPartnershipMember] shown=— → 0
- …InYearFour ctx=C_11480f13-b944-49b7-8e9d-1578b92c43f5 [LegalEntityAxis=UnconsolidatedInvestmentsinPartnershipMember] shown=107,289 → 107,289,000
- …InYearFour ctx=C_731fe8d0-f215-468c-a36d-1b69136cf186 [LegalEntityAxis=UnconsolidatedInvestmentsinPartnershipProRataShareMemberMember] shown=37,157 → 37,157,000
- …InYearFive ctx=C_3070f302-beaf-4288-8fda-553462736cb6 [LegalEntityAxis=UnconsolidatedInvestmentsinPartnershipMember; LongtermDebtTypeAxis=MortgagesMember; ScheduledPrincipalPaymentsAndMaturitiesAxis=ScheduledPrincipalPaymentsMember] shown=2,349 → 2,349,000
- …InYearFive ctx=C_e87b8439-8bfa-4403-92d5-03ff6677297a [LongtermDebtTypeAxis=MortgagesMember; LegalEntityAxis=UnconsolidatedInvestmentsinPartnershipMember; ScheduledPrincipalPaymentsAndMaturitiesAxis=MortgageLoanMaturitiesMember] shown=215,893 → 215,893,000
- …InYearFive ctx=C_5fae9eb1-f2d4-4a99-a50a-35fd8bd99cd6 [LongtermDebtTypeAxis=UnsecuredDebtMember; ScheduledPrincipalPaymentsAndMaturitiesAxis=UnsecuredMaturitiesMember; LegalEntityAxis=UnconsolidatedInvestmentsinPartnershipMember] shown=— → 0
- …InYearFive ctx=C_11480f13-b944-49b7-8e9d-1578b92c43f5 [LegalEntityAxis=UnconsolidatedInvestmentsinPartnershipMember] shown=218,242 → 218,242,000
- …InYearFive ctx=C_731fe8d0-f215-468c-a36d-1b69136cf186 [LegalEntityAxis=UnconsolidatedInvestmentsinPartnershipProRataShareMemberMember] shown=77,886 → 77,886,000
- …AfterYearFive ctx=C_3070f302-beaf-4288-8fda-553462736cb6 [LegalEntityAxis=UnconsolidatedInvestmentsinPartnershipMember; LongtermDebtTypeAxis=MortgagesMember; ScheduledPrincipalPaymentsAndMaturitiesAxis=ScheduledPrincipalPaymentsMember] shown=2,159 → 2,159,000
- …AfterYearFive ctx=C_e87b8439-8bfa-4403-92d5-03ff6677297a [LongtermDebtTypeAxis=MortgagesMember; LegalEntityAxis=UnconsolidatedInvestmentsinPartnershipMember; ScheduledPrincipalPaymentsAndMaturitiesAxis=MortgageLoanMaturitiesMember] shown=634,631 → 634,631,000
- …AfterYearFive ctx=C_5fae9eb1-f2d4-4a99-a50a-35fd8bd99cd6 [LongtermDebtTypeAxis=UnsecuredDebtMember; ScheduledPrincipalPaymentsAndMaturitiesAxis=UnsecuredMaturitiesMember; LegalEntityAxis=UnconsolidatedInvestmentsinPartnershipMember] shown=— → 0
- …AfterYearFive ctx=C_11480f13-b944-49b7-8e9d-1578b92c43f5 [LegalEntityAxis=UnconsolidatedInvestmentsinPartnershipMember] shown=636,790 → 636,790,000
- …AfterYearFive ctx=C_731fe8d0-f215-468c-a36d-1b69136cf186 [LegalEntityAxis=UnconsolidatedInvestmentsinPartnershipProRataShareMemberMember] shown=237,869 → 237,869,000

### Kimco Realty
NOT DONE: n/a: no ladder tags at 2025-12-31 in companyfacts, so there is nothing to compare (no 10-K table was parsed or guessed)

### Federal Realty
Source: https://www.sec.gov/Archives/edgar/data/34903/000003490326000017/frt-20251231.htm

Method: the inline-XBRL facts rendered *inside the 10-K document* (dimensionless context, instant 2025-12-31), displayed number × 10^scale, compared with the companyfacts value.

| bucket | tag | extracted (companyfacts) | 10-K displayed → USD | shown text | diff | note |
|---|---|---:|---:|---|---:|---|
| y1_2026 | …InNextTwelveMonths | 655,595,000 | 655,595,000 | 655,595 (scale 3) | 0 |  |
| y2_2027 | …InYearTwo | 1,003,319,000 | 1,003,319,000 | 1,003,319 (scale 3) | 0 |  |
| y3_2028 | …InYearThree | 1,157,511,000 | 1,157,511,000 | 1,157,511 (scale 3) | 0 |  |
| y4_2029 | …InYearFour | 945,434,000 | 945,434,000 | 945,434 (scale 3) | 0 |  |
| y5_2030 | …InYearFive | 400,684,000 | 400,684,000 | 400,684 (scale 3) | 0 |  |
| after_2030 | …AfterYearFive | 801,059,000 | 801,059,000 | 801,059 (scale 3) | 0 |  |

Table as rendered in the 10-K (cells joined with |; '$' cells dropped):

```
Mortgages Payable | Notes Payable | Senior Notes and Debentures | Total Principal
(In thousands)
Year ending December 31,
2026 | 226,242 | (1) | 153 | 429,200 | 655,595
2027 | 178,282 | 310,037 | (2) | 515,000 | 1,003,319
2028 | 57,511 | (3) | 750,000 | (4) | 350,000 | 1,157,511
2029 | 60,434 | — | 885,000 | 945,434
2030 | 684 | — | 400,000 | 400,684
Thereafter | 59 | 1,000 | 800,000 | 801,059
523,212 | 1,061,190 | 3,379,200 | 4,963,602 | (5)
```

Printed total in the table ('(unlabelled subtotal row)', ladder column): 4,963,602 (scale 3) = 4,963,602,000; six tagged buckets sum to 4,963,602,000; diff 0.

2027 bucket by XBRL dimension (INFERRED: column meaning taken from the filer's member names, not yet confirmed by a human against the table header):

| kind | member | unsecured bank/notes? | shown | USD |
|---|---|---|---:|---:|
| instrument | SecuredDebtMember | False | 178,282 | 178,282,000 |
| instrument | NotesPayableOtherPayablesMember | False | 310,037 | 310,037,000 |
| instrument | SeniorNotesMember | True | 515,000 | 515,000,000 |

Dimensioned ladder facts in the same filing (not in companyfacts totals, shown for the reader): 18

- …InNextTwelveMonths ctx=c-213 [LongtermDebtTypeAxis=SecuredDebtMember] shown=226,242 → 226,242,000
- …InNextTwelveMonths ctx=c-224 [LongtermDebtTypeAxis=NotesPayableOtherPayablesMember] shown=153 → 153,000
- …InNextTwelveMonths ctx=c-246 [LongtermDebtTypeAxis=SeniorNotesMember] shown=429,200 → 429,200,000
- …InYearTwo ctx=c-213 [LongtermDebtTypeAxis=SecuredDebtMember] shown=178,282 → 178,282,000
- …InYearTwo ctx=c-224 [LongtermDebtTypeAxis=NotesPayableOtherPayablesMember] shown=310,037 → 310,037,000
- …InYearTwo ctx=c-246 [LongtermDebtTypeAxis=SeniorNotesMember] shown=515,000 → 515,000,000
- …InYearThree ctx=c-213 [LongtermDebtTypeAxis=SecuredDebtMember] shown=57,511 → 57,511,000
- …InYearThree ctx=c-224 [LongtermDebtTypeAxis=NotesPayableOtherPayablesMember] shown=750,000 → 750,000,000
- …InYearThree ctx=c-246 [LongtermDebtTypeAxis=SeniorNotesMember] shown=350,000 → 350,000,000
- …InYearFour ctx=c-213 [LongtermDebtTypeAxis=SecuredDebtMember] shown=60,434 → 60,434,000
- …InYearFour ctx=c-224 [LongtermDebtTypeAxis=NotesPayableOtherPayablesMember] shown=— → 0
- …InYearFour ctx=c-246 [LongtermDebtTypeAxis=SeniorNotesMember] shown=885,000 → 885,000,000
- …InYearFive ctx=c-213 [LongtermDebtTypeAxis=SecuredDebtMember] shown=684 → 684,000
- …InYearFive ctx=c-224 [LongtermDebtTypeAxis=NotesPayableOtherPayablesMember] shown=— → 0
- …InYearFive ctx=c-246 [LongtermDebtTypeAxis=SeniorNotesMember] shown=400,000 → 400,000,000
- …AfterYearFive ctx=c-213 [LongtermDebtTypeAxis=SecuredDebtMember] shown=59 → 59,000
- …AfterYearFive ctx=c-224 [LongtermDebtTypeAxis=NotesPayableOtherPayablesMember] shown=1,000 → 1,000,000
- …AfterYearFive ctx=c-246 [LongtermDebtTypeAxis=SeniorNotesMember] shown=800,000 → 800,000,000

### Macerich
NOT DONE: n/a: no ladder tags at 2025-12-31 in companyfacts, so there is nothing to compare (no 10-K table was parsed or guessed)

### Tanger
NOT DONE: n/a: no ladder tags at 2025-12-31 in companyfacts, so there is nothing to compare (no 10-K table was parsed or guessed)

### Phillips Edison
Source: https://www.sec.gov/Archives/edgar/data/1476204/000147620426000005/cik0001476204-20251231.htm

Method: the inline-XBRL facts rendered *inside the 10-K document* (dimensionless context, instant 2025-12-31), displayed number × 10^scale, compared with the companyfacts value.

| bucket | tag | extracted (companyfacts) | 10-K displayed → USD | shown text | diff | note |
|---|---|---:|---:|---|---:|---|
| y1_2026 | …InNextTwelveMonths | 163,654,000 | 163,654,000 | 163,654 (scale 3) | 0 |  |
| y2_2027 | …InYearTwo | 523,595,000 | 523,595,000 | 523,595 (scale 3) | 0 |  |
| y3_2028 | …InYearThree | 17,367,000 | 17,367,000 | 17,367 (scale 3) | 0 |  |
| y4_2029 | …InYearFour | 92,805,000 | 92,805,000 | 92,805 (scale 3) | 0 |  |
| y5_2030 | …InYearFive | 200,844,000 | 200,844,000 | 200,844 (scale 3) | 0 |  |
| after_2030 | …AfterYearFive | 1,403,400,000 | 1,403,400,000 | 1,403,400 (scale 3) | 0 |  |

Table as rendered in the 10-K (cells joined with |; '$' cells dropped):

```
2026 | 2027 | 2028 | 2029 | 2030 | Thereafter | Total
Unsecured debt(1)(2) | 161,750 | 323,000 | — | 92,000 | — | 1,400,000 | 1,976,750
Secured debt | 1,904 | 200,595 | 17,367 | 805 | 200,844 | 3,400 | 424,915
Total | 163,654 | 523,595 | 17,367 | 92,805 | 200,844 | 1,403,400 | 2,401,665
```

Printed total: NOT FOUND. The row directly below the year rows is neither labelled 'Total' nor an unlabelled subtotal with a number in the ladder column. Not guessed.

2027 bucket by XBRL dimension (INFERRED: column meaning taken from the filer's member names, not yet confirmed by a human against the table header):

| kind | member | unsecured bank/notes? | shown | USD |
|---|---|---|---:|---:|
| instrument | UnsecuredDebtMember | True | 323,000 | 323,000,000 |
| instrument | SecuredDebtMember | False | 200,595 | 200,595,000 |

Dimensioned ladder facts in the same filing (not in companyfacts totals, shown for the reader): 12

- …InNextTwelveMonths ctx=c-160 [LongtermDebtTypeAxis=UnsecuredDebtMember] shown=161,750 → 161,750,000
- …InYearTwo ctx=c-160 [LongtermDebtTypeAxis=UnsecuredDebtMember] shown=323,000 → 323,000,000
- …InYearThree ctx=c-160 [LongtermDebtTypeAxis=UnsecuredDebtMember] shown=— → 0
- …InYearFour ctx=c-160 [LongtermDebtTypeAxis=UnsecuredDebtMember] shown=92,000 → 92,000,000
- …InYearFive ctx=c-160 [LongtermDebtTypeAxis=UnsecuredDebtMember] shown=— → 0
- …AfterYearFive ctx=c-160 [LongtermDebtTypeAxis=UnsecuredDebtMember] shown=1,400,000 → 1,400,000,000
- …InNextTwelveMonths ctx=c-165 [LongtermDebtTypeAxis=SecuredDebtMember] shown=1,904 → 1,904,000
- …InYearTwo ctx=c-165 [LongtermDebtTypeAxis=SecuredDebtMember] shown=200,595 → 200,595,000
- …InYearThree ctx=c-165 [LongtermDebtTypeAxis=SecuredDebtMember] shown=17,367 → 17,367,000
- …InYearFour ctx=c-165 [LongtermDebtTypeAxis=SecuredDebtMember] shown=805 → 805,000
- …InYearFive ctx=c-165 [LongtermDebtTypeAxis=SecuredDebtMember] shown=200,844 → 200,844,000
- …AfterYearFive ctx=c-165 [LongtermDebtTypeAxis=SecuredDebtMember] shown=3,400 → 3,400,000

**Ladders checked number by number against 10-K text: SL Green, Cousins Properties, JBG Smith, Piedmont Office, Office Properties Income Trust, Empire State Realty Trust, CBL & Associates, Simon Property Group, Brixmor, Acadia Realty, Kite Realty, Kilroy Realty, Highwoods Properties, Brandywine Realty Trust, Regency Centers, Federal Realty, Phillips Edison.**

Not checked against 10-K text (companyfacts vs frames only): BXP, Vornado Realty Trust, Douglas Emmett, Hudson Pacific Properties, Kimco Realty, Macerich, Tanger.

## 3b. Filing list check: SL Green, all forms, 2026-03-10 to 2026-03-31

Question: Is there any SLG filing for the March 18, 2026 credit facility amendment?

Source: https://data.sec.gov/submissions/CIK0001040971.json (cached 20261109T021822Z)

| filed | form | items | accession |
|---|---|---|---|
| 2026-03-30 | 4 | none | 0001916385-26-000002 |
| 2026-03-30 | 144 | none | 0001957799-26-000044 |
| 2026-03-26 | SCHEDULE 13G/A | none | 0000102909-26-000468 |
| 2026-03-10 | 4 | none | 0002117999-26-000004 |
| 2026-03-10 | 3 | none | 0002117999-26-000003 |

**Result: 5 filings in the window, 0 of them 8-K.** All 2026 8-Ks with their items: 2026-10-22 [2.02,7.01,9.01]; 2026-07-23 [2.02,7.01,9.01]; 2026-06-02 [5.07]; 2026-04-16 [2.02,7.01,9.01]; 2026-03-06 [1.01,3.02,9.01]; 2026-03-04 [5.02,9.01]; 2026-01-29 [2.02,7.01,9.01].
The exhibits of the earnings 8-Ks (items 2.02/7.01) are searched in §3d below.

## 3d. Exhibit search: SL Green 8-Ks with item(s) 2.02 since 2026-01-01

Question: Does any SLG 2026 earnings 8-K exhibit mention the March 2026 credit facility amendment?
Pattern (case-insensitive): `credit facilit|term loan|revolving credit|amended and restated|2026 Credit Facility|March 2026`

### 8-K filed 2026-01-29 (0001628280-26-004077): documents searched a25q4earningsrelease.htm, a25q4supplemental.htm (cover slg-20260128.htm excluded)

- a25q4earningsrelease.htm (https://www.sec.gov/Archives/edgar/data/1040971/000162828026004077/a25q4earningsrelease.htm): **1 matching sentence(s)**
  - “CONSOLIDATED BALANCE SHEETS (unaudited and in thousands, except per share data) December 31, December 31, 2025 2024 Assets Commercial real estate properties, at cost: Land and land interests $ 1,699,215 $ 1,357,041 Building and improvements 4,012,305 3,862,224 Building leasehold and improvements 1,448,112 1,388,476 7,159,632 6,607,741 Less: accumulated depreciation (2,306,377) (2,126,081) 4,853,255 4,481,660 Cash and cash equivalents 155,747 184,294 Restricted cash 180,748 147,344 Investment in marketable securities 23,666 22,812 Tenant and other receivables 45,524 44,055 Related party receivables 16,293 26,865 Deferred rents receivable 266,678 266,428 Debt and preferred equity investments, ”

- a25q4supplemental.htm (https://www.sec.gov/Archives/edgar/data/1040971/000162828026004077/a25q4supplemental.htm): **5 matching sentence(s)**
  - “The calculation of fixed charge coverage for purposes of our credit facility covenants is governed by the terms of the credit facility.”
  - “Supplemental Information 11 Fourth Quarter 2025 COMPARATIVE BALANCE SHEETS Unaudited (Dollars in Thousands) As of 12/31/2025 9/30/2025 6/30/2025 3/31/2025 12/31/2024 Assets Commercial real estate properties, at cost: Land and land interests $ 1,699,215 $ 1,627,895 $ 1,448,504 $ 1,450,892 $ 1,357,041 Building and improvements 4,012,305 4,082,434 3,867,078 3,828,638 3,862,224 Building leasehold and improvements 1,448,112 1,424,907 1,415,754 1,399,376 1,388,476 7,159,632 7,135,236 6,731,336 6,678,906 6,607,741 Less: accumulated depreciation (2,306,377) (2,266,042) (2,220,242) (2,174,667) (2,126,081) Net real estate 4,853,255 4,869,194 4,511,094 4,504,239 4,481,660 Other real estate investments:”
  - “Supplemental Information 23 Fourth Quarter 2025 DEBT SUMMARY SCHEDULE Consolidated Unaudited (Dollars in Thousands) Principal 2026 Current Final Principal Ownership Outstanding Principal Maturity Maturity Due at Fixed rate debt Interest (%) 12/31/2025 Coupon (1) Amortization Date Date (2) Final Maturity Secured fixed rate debt 10 East 53rd Street (swapped) 100.0 $ 204,550 5.37% $ — May-26 May-28 (3) $ 204,550 185 Broadway / 7 Dey Street 100.0 190,149 6.35% — Nov-26 Nov-26 190,149 100 Church Street (swapped) 100.0 365,000 5.89% — Dec-26 Jun-28 365,000 Landmark Square 100.0 100,000 4.90% — Jan-27 Jan-27 100,000 485 Lexington Avenue 100.0 450,000 4.25% — Feb-27 Feb-27 450,000 315 W 33rd St (The”
  - “Supplemental Information 25 Fourth Quarter 2025 DEBT COMPOSITION AND CORPORATE DEBT COVENANTS Unaudited (Dollars in Thousands) Composition of Debt Core Portfolio Alternative Strategy Portfolio Total Fixed Rate Debt Consolidated $ 3,678,450 $ — $ 3,678,450 SLG Share of JV 5,414,546 366,531 5,781,077 Total Fixed Rate Debt $ 9,092,996 96.1% $ 366,531 76.6% $ 9,459,527 95.2% Floating Rate Debt Consolidated $ 366,049 $ — $ 366,049 SLG Share of JV 4,221 111,900 116,121 370,270 3.9% 111,900 23.4% 482,170 4.8% Debt & Preferred Equity and CMBS Investments (128,619) (1.4)% — —% (128,619) (1.3)% Total Floating Rate Debt $ 241,651 2.6% $ 111,900 23.4% $ 353,551 3.6% Total Debt $ 9,463,266 $ 478,431 $ 9,”
  - “Supplemental Information 26 Fourth Quarter 2025 DERIVATIVE SUMMARY SCHEDULE Unaudited (Dollars in Thousands) Consolidated Interest Rate Derivatives Ownership Notional Value Fair Value Secured Debt Interest (%) 12/31/2025 12/31/2025 Instrument (1) Strike Rate (1) Effective Date Maturity Date 800 Third Avenue 100.0 $177,000 $486 Swap 1.55 % December 2022 February 2026 185 Broadway 100.0 $190,148 193 Cap 3.50 % November 2025 November 2026 100 Church Street 100.0 $370,000 (3,076) Swap 3.89 % November 2022 June 2027 SLGOP – 450 Park Avenue 100.0 $68,678 (1,167) (2) Swap 4.47 % August 2024 June 2027 SLGOP – One Madison Avenue 100.0 $300,000 (6,521) (2) Swap 4.49 % November 2024 November 2027 500 P”

### 8-K filed 2026-04-16 (0001628280-26-025419): documents searched a26q1earningsrelease.htm, a26q1supplemental.htm (cover slg-20260415.htm excluded)

- a26q1earningsrelease.htm (https://www.sec.gov/Archives/edgar/data/1040971/000162828026025419/a26q1earningsrelease.htm): **9 matching sentence(s)**
  - “•Refinanced, extended and reduced the overall cost of $2.0 billion of the Company's $2.4 billion corporate credit facility.”
  - “The existing $1.25 billion revolving line of credit was extended to June 2031 while the existing $1.05 billion term loan was bifurcated, resulting in a new $750 million term loan with a maturity date of June 2031.”
  - “The cost of the revolving line of credit and the new term loan were each reduced by 25 basis points.”
  - “The remaining $300 million term loan that matures in May 2027 and the existing $100 million term loan that matures in November 2026 were not modified.”
  - “In March, the Company refinanced, extended and reduced the overall cost of $2.0 billion of the Company's $2.4 billion corporate credit facility.”
  - “•The existing $1.05 billion term loan component of the facility was bifurcated, resulting in a new $750 million term loan with a maturity date of June 2031 and a borrowing cost that was reduced by 25 basis points to 145 basis points over SOFR, based on the Company’s current credit rating.”
  - “The remaining $300 million of the term loan with a maturity date of May 2027 will continue to be outstanding on its current terms.”
  - “•The existing $100 million term loan component of the facility with a maturity date of November 2026 will also remain outstanding on its current terms.”
  - “CONSOLIDATED BALANCE SHEETS (unaudited and in thousands, except per share data) March 31, December 31, 2026 2025 Assets Commercial real estate properties, at cost: Land and land interests $ 1,848,531 $ 1,699,215 Building and improvements 4,298,249 4,012,305 Building leasehold and improvements 1,465,411 1,448,112 7,612,191 7,159,632 Less: accumulated depreciation (2,321,290) (2,306,377) 5,290,901 4,853,255 Assets held for sale 211,222 — Cash and cash equivalents 143,867 155,747 Restricted cash 194,772 180,748 Investment in marketable securities 25,330 23,666 Tenant and other receivables 56,724 45,524 Related party receivables 25,161 16,293 Deferred rents receivable 262,730 266,678 Debt and pr”

- a26q1supplemental.htm (https://www.sec.gov/Archives/edgar/data/1040971/000162828026025419/a26q1supplemental.htm): **9 matching sentence(s)**
  - “The calculation of fixed charge coverage for purposes of our credit facility covenants is governed by the terms of the credit facility.”
  - “In March, the Company refinanced, extended and reduced the overall cost of $2.0 billion of the Company's $2.4 billion corporate credit facility.”
  - “•The existing $1.05 billion term loan component of the facility was bifurcated, resulting in a new $750 million term loan with a maturity date of June 2031 and a borrowing cost that was reduced by 25 basis points to 145 basis points over SOFR, based on the Company’s current credit rating.”
  - “The remaining $300 million of the term loan with a maturity date of May 2027 will continue to be outstanding on its current terms.”
  - “•The existing $100 million term loan component of the facility with a maturity date of November 2026 will also remain outstanding on its current terms.”
  - “Supplemental Information 11 First Quarter 2026 COMPARATIVE BALANCE SHEETS Unaudited (Dollars in Thousands) As of 3/31/2026 12/31/2025 9/30/2025 6/30/2025 3/31/2025 Assets Commercial real estate properties, at cost: Land and land interests $ 1,848,531 $ 1,699,215 $ 1,627,895 $ 1,448,504 $ 1,450,892 Building and improvements 4,298,249 4,012,305 4,082,434 3,867,078 3,828,638 Building leasehold and improvements 1,465,411 1,448,112 1,424,907 1,415,754 1,399,376 7,612,191 7,159,632 7,135,236 6,731,336 6,678,906 Less: accumulated depreciation (2,321,290) (2,306,377) (2,266,042) (2,220,242) (2,174,667) Net real estate 5,290,901 4,853,255 4,869,194 4,511,094 4,504,239 Other real estate investments: D”
  - “Supplemental Information 22 First Quarter 2026 DEBT SUMMARY SCHEDULE Consolidated Unaudited (Dollars in Thousands) Principal 2026 Current Final Principal Ownership Outstanding Principal Maturity Maturity Due at Fixed rate debt Interest (%) 3/31/2026 Coupon (1) Amortization Date Date (2) Final Maturity Secured fixed rate debt 10 East 53rd Street (swapped) 100.0 $ 204,438 5.37% $ — May-26 May-28 (3) $ 204,438 7 Dey Street (4) 100.0 190,148 6.35% — Nov-26 Nov-26 190,148 100 Church Street (swapped) 100.0 365,000 5.89% — Dec-26 Jun-28 365,000 Landmark Square 100.0 100,000 4.90% — Jan-27 Jan-27 100,000 485 Lexington Avenue 100.0 450,000 4.25% — Feb-27 Feb-27 450,000 315 W 33rd St (The Olivia) (5) ”
  - “Supplemental Information 24 First Quarter 2026 DEBT COMPOSITION AND CORPORATE DEBT COVENANTS Unaudited (Dollars in Thousands) Composition of Debt Core Portfolio Alternative Strategy Portfolio Total Fixed Rate Debt Consolidated $ 4,108,672 $ — $ 4,108,672 SLG Share of JV 5,263,980 366,531 5,630,511 Total Fixed Rate Debt $ 9,372,652 91.1% $ 366,531 76.6% $ 9,739,183 90.4% Floating Rate Debt Consolidated $ 665,611 $ — $ 665,611 SLG Share of JV 255,000 111,900 366,900 920,611 8.9% 111,900 23.4% 1,032,511 9.6% Debt & Preferred Equity and CMBS Investments (78,594) (0.8)% — —% (78,594) (0.7)% Total Floating Rate Debt $ 842,017 8.2% $ 111,900 23.4% $ 953,917 8.9% Total Debt $ 10,293,263 $ 478,431 $ ”
  - “Supplemental Information 25 First Quarter 2026 DERIVATIVE SUMMARY SCHEDULE Unaudited (Dollars in Thousands) Consolidated Interest Rate Derivatives Notional Value Fair Value Ownership 3/31/2026 3/31/2026 Secured Debt Interest (%) Gross SLG Share Gross SLG Share Instrument (1) Strike Rate (1) Effective Date Maturity Date 7 Dey Street 100.0 $190,148 $190,148 $289 $289 Cap 3.50 % November 2025 November 2026 100 Church Street 100.0 370,000 370,000 (1,132) (1,132) Swap 3.89 % November 2022 June 2027 SLGOP – 450 Park Avenue 100.0 68,678 68,678 (701) (701) (2) Swap 4.47 % August 2024 June 2027 SLGOP – 450 Park Avenue 100.0 4,221 4,221 (59) (59) (2) Swap 4.49 % November 2024 November 2027 500 Park Av”

### 8-K filed 2026-07-23 (0001628280-26-049346): documents searched a26q2earningsrelease.htm, a26q2supplemental.htm (cover slg-20260722.htm excluded)

- a26q2earningsrelease.htm (https://www.sec.gov/Archives/edgar/data/1040971/000162828026049346/a26q2earningsrelease.htm): **1 matching sentence(s)**
  - “CONSOLIDATED BALANCE SHEETS (unaudited and in thousands, except per share data) June 30, December 31, 2026 2025 Assets Commercial real estate properties, at cost: Land and land interests $ 1,579,973 $ 1,699,215 Building and improvements 4,272,142 4,012,305 Building leasehold and improvements 1,478,991 1,448,112 7,331,106 7,159,632 Less: accumulated depreciation (2,359,905) (2,306,377) 4,971,201 4,853,255 Assets held for sale 214,586 — Cash and cash equivalents 180,788 155,747 Restricted cash 200,961 180,748 Investment in marketable securities 21,273 23,666 Tenant and other receivables 60,180 45,524 Related party receivables 13,867 16,293 Deferred rents receivable 262,008 266,678 Debt and pre”

- a26q2supplemental.htm (https://www.sec.gov/Archives/edgar/data/1040971/000162828026049346/a26q2supplemental.htm): **5 matching sentence(s)**
  - “The calculation of fixed charge coverage for purposes of our credit facility covenants is governed by the terms of the credit facility.”
  - “Supplemental Information 12 Second Quarter 2026 COMPARATIVE BALANCE SHEETS Unaudited (Dollars in Thousands) As of 6/30/2026 3/31/2026 12/31/2025 9/30/2025 6/30/2025 Assets Commercial real estate properties, at cost: Land and land interests $ 1,579,973 $ 1,848,531 $ 1,699,215 $ 1,627,895 $ 1,448,504 Building and improvements 4,272,142 4,298,249 4,012,305 4,082,434 3,867,078 Building leasehold and improvements 1,478,991 1,465,411 1,448,112 1,424,907 1,415,754 7,331,106 7,612,191 7,159,632 7,135,236 6,731,336 Less: accumulated depreciation (2,359,905) (2,321,290) (2,306,377) (2,266,042) (2,220,242) Net real estate 4,971,201 5,290,901 4,853,255 4,869,194 4,511,094 Other real estate investments: ”
  - “Supplemental Information 24 Second Quarter 2026 DEBT SUMMARY SCHEDULE Consolidated Unaudited (Dollars in Thousands) Principal 2026 Current Final Principal Ownership Outstanding Principal Maturity Maturity Due at Fixed rate debt Interest (%) 6/30/2026 Coupon (1) Amortization Date Date (2) Final Maturity Secured fixed rate debt 100 Church Street (swapped) 100.0 $ 365,000 5.89% $ — Dec-26 Jun-28 $ 365,000 Landmark Square 100.0 100,000 4.90% — Jan-27 Jan-27 100,000 485 Lexington Avenue 100.0 450,000 4.25% — Feb-27 Feb-27 450,000 315 West 33rd St (The Olivia) (3) 100.0 250,000 4.24% — Feb-27 Feb-27 250,000 10 East 53rd Street (swapped) (4) 100.0 204,325 5.37% — May-27 May-28 (5) 204,325 500 Park ”
  - “Supplemental Information 26 Second Quarter 2026 DEBT COMPOSITION AND CORPORATE DEBT COVENANTS Unaudited (Dollars in Thousands) Composition of Debt Core Portfolio Alternative Strategy Portfolio Total Fixed Rate Debt Consolidated $ 3,619,708 $ — $ 3,619,708 SLG Share of JV 5,256,353 367,041 5,623,394 Total Fixed Rate Debt $ 8,876,061 88.2% $ 367,041 77.8% $ 9,243,102 87.7% Floating Rate Debt Consolidated $ 929,422 $ — $ 929,422 SLG Share of JV 259,221 105,000 364,221 1,188,643 11.8% 105,000 22.2% 1,293,643 12.3% Debt & Preferred Equity and CMBS Investments (78,543) (0.8)% — —% (78,543) (0.7)% Total Floating Rate Debt $ 1,110,100 11.0% $ 105,000 22.2% $ 1,215,100 11.5% Total Debt $ 10,064,704 $”
  - “Supplemental Information 27 Second Quarter 2026 DERIVATIVE SUMMARY SCHEDULE Unaudited (Dollars in Thousands) Consolidated Interest Rate Derivatives Notional Value Fair Value Ownership 6/30/2026 6/30/2026 Secured Debt Interest (%) Gross SLG Share Gross SLG Share Instrument (1) Strike Rate (1) Effective Date Maturity Date 100 Church Street 100.0 $370,000 $370,000 $165 $165 Swap 3.89 % November 2022 June 2027 SLGOP - 450 Park Avenue 100.0 68,678 68,678 (354) (354) (2) Swap 4.47 % August 2024 June 2027 500 Park Avenue 100.0 80,000 80,000 (278) (278) Swap 4.17 % February 2025 February 2028 10 East 53rd Street 100.0 204,325 204,325 114 114 Swap 3.92 % February 2025 May 2028 800 Third Avenue 100.0 ”

### 8-K filed 2026-10-22 (0001628280-26-066842): documents searched a26q3earningsrelease.htm, a26q3supplemental.htm (cover slg-20261021.htm excluded)

- a26q3earningsrelease.htm (https://www.sec.gov/Archives/edgar/data/1040971/000162828026066842/a26q3earningsrelease.htm): **1 matching sentence(s)**
  - “CONSOLIDATED BALANCE SHEETS (unaudited and in thousands, except per share data) September 30, December 31, 2026 2025 Assets Commercial real estate properties, at cost: Land and land interests $ 1,534,127 $ 1,699,215 Building and improvements 4,068,129 4,012,305 Building leasehold and improvements 1,496,428 1,448,112 7,098,684 7,159,632 Less: accumulated depreciation (2,333,095) (2,306,377) 4,765,589 4,853,255 Assets held for sale 224,249 — Cash and cash equivalents 186,439 155,747 Restricted cash 199,507 180,748 Investment in marketable securities 21,166 23,666 Tenant and other receivables 64,072 45,524 Related party receivables 17,195 16,293 Deferred rents receivable 255,497 266,678 Debt an”

- a26q3supplemental.htm (https://www.sec.gov/Archives/edgar/data/1040971/000162828026066842/a26q3supplemental.htm): **5 matching sentence(s)**
  - “The calculation of fixed charge coverage for purposes of our credit facility covenants is governed by the terms of the credit facility.”
  - “Supplemental Information 12 Third Quarter 2026 COMPARATIVE BALANCE SHEETS Unaudited (Dollars in Thousands) As of 9/30/2026 6/30/2026 3/31/2026 12/31/2025 9/30/2025 Assets Commercial real estate properties, at cost: Land and land interests $ 1,534,127 $ 1,579,973 $ 1,848,531 $ 1,699,215 $ 1,627,895 Building and improvements 4,068,129 4,272,142 4,298,249 4,012,305 4,082,434 Building leasehold and improvements 1,496,428 1,478,991 1,465,411 1,448,112 1,424,907 7,098,684 7,331,106 7,612,191 7,159,632 7,135,236 Less: accumulated depreciation (2,333,095) (2,359,905) (2,321,290) (2,306,377) (2,266,042) Net real estate 4,765,589 4,971,201 5,290,901 4,853,255 4,869,194 Other real estate investments: D”
  - “Supplemental Information 24 Third Quarter 2026 DEBT SUMMARY SCHEDULE Consolidated Unaudited (Dollars in Thousands) Principal 2026 Current Final Principal Ownership Outstanding Principal Maturity Maturity Due at Fixed rate debt Interest (%) 9/30/2026 Coupon (1) Amortization Date Date (2) Final Maturity Secured fixed rate debt 100 Church Street (swapped) 100.0 $ 365,000 5.89% $ — Dec-26 Jun-28 $ 365,000 Landmark Square 100.0 100,000 4.90% — Jan-27 Jan-27 100,000 485 Lexington Avenue 100.0 450,000 4.25% — Feb-27 Feb-27 450,000 315 West 33rd St (The Olivia) (3) 100.0 250,000 4.24% — Feb-27 Feb-27 250,000 500 Park Avenue (swapped) 100.0 80,000 6.57% — Jan-28 Jan-30 80,000 800 Third Avenue (swappe”
  - “Supplemental Information 26 Third Quarter 2026 DEBT COMPOSITION AND CORPORATE DEBT COVENANTS Unaudited (Dollars in Thousands) Composition of Debt Core Portfolio Alternative Strategy Portfolio Total Fixed Rate Debt Consolidated $ 3,409,386 $ — $ 3,409,386 SLG Share of JV 5,252,912 367,077 5,619,989 Total Fixed Rate Debt $ 8,662,298 87.4% $ 367,077 77.8% $ 9,029,375 87.0% Floating Rate Debt Consolidated $ 987,413 $ — $ 987,413 SLG Share of JV 259,221 105,000 364,221 1,246,634 12.6% 105,000 22.2% 1,351,634 13.0% Debt & Preferred Equity and CMBS Investments (78,553) (0.8)% — —% (78,553) (0.8)% Total Floating Rate Debt $ 1,168,081 11.8% $ 105,000 22.2% $ 1,273,081 12.3% Total Debt $ 9,908,932 $ 4”
  - “Supplemental Information 27 Third Quarter 2026 DERIVATIVE SUMMARY SCHEDULE Unaudited (Dollars in Thousands) Consolidated Interest Rate Derivatives Notional Value Fair Value Ownership 9/30/2026 9/30/2026 Secured Debt Interest (%) Gross SLG Share Gross SLG Share Instrument (1) Strike Rate (1) Effective Date Maturity Date 100 Church Street 100.0 $370,000 $370,000 $1,051 $1,051 Swap 3.89 % November 2022 June 2027 SLGOP - 450 Park Avenue 100.0 68,678 68,678 (80) (80) (2) Swap 4.47 % August 2024 June 2027 500 Park Avenue 100.0 80,000 80,000 388 388 Swap 4.17 % February 2025 February 2028 800 Third Avenue 100.0 177,000 177,000 5,281 5,281 Swap 3.33 % February 2026 February 2029 Subtotal $6,640 $6,6”

**Total matching sentences across 4 earnings 8-K(s): 36.**

## 3c. SLG column mapping: arithmetic confirmation (stays INFERRED until signed off)

10-Q header column 3 = 'Unsecured Term Loans'. Non-zero cells: Remaining 2026: 100,000, 2027: 300,000, Thereafter: 750,000. Sum = 1,150,000; printed column total = 1,150,000; **equal**.

10-Q text names Term B $100.0M, Term A $300.0M, Term C $750.0M: **matches the column cells**.

10-K 2027 cell tagged TermLoanMember = 1,050,000,000; 10-K text: 'May 15, 2027: As of December 31, 2025, the 2021 credit facility consisted of a $1.25 billion revolving credit facility, a $1.05 billion term loan (or "Term Loan…' → **consistent: Term Loan A $1.05B due May 15, 2027**.

## 4. Control total

Primary: the 10-K table's printed Total (spot-checked names only). Secondary: LongTermDebt.

| name | ladder sum | 10-K printed total | diff | LongTermDebt @2025-12-31 | diff | latest LongTermDebt (end) | diff |
|---|---:|---:|---:|---:|---:|---:|---:|
| SL Green | 4,044,499,000 | 4,044,499,000 | 0 | n/a | n/a | 3,227,563,000 (2022-12-31, STALE) | 816,936,000 |
| Cousins Properties | 3,357,127,000 | 3,357,127,000 | 0 | 3,340,815,000 | 16,312,000 | 3,579,763,000 (2026-09-30) | -222,636,000 |
| JBG Smith | 2,546,589,000 (incomplete) | 2,546,589,000 | 0 | n/a | n/a | 1,376,077,000 (2017-06-30, STALE) | 1,170,512,000 |
| Piedmont Office | 2,248,080,000 | 2,248,080,000 | 0 | 2,224,712,000 | 23,368,000 | 2,340,841,000 (2026-09-30) | -92,761,000 |
| Office Properties Income Trust | 2,431,614,000 | 2,431,614,000 | 0 | 2,408,626,000 | 22,988,000 | 1,683,556,000 (2026-06-30) | 748,058,000 |
| Empire State Realty Trust | 2,389,011,000 | 2,389,011,000 | 0 | n/a | n/a | 606,313,000 (2019-09-30, STALE) | 1,782,698,000 |
| BXP | n/a (incomplete) | not checked | n/a | n/a | n/a | 3,300,000,000 (2021-12-31, STALE) | n/a |
| CBL & Associates | 2,224,398,195 | 2,235,582,000 | -11,183,805 | 2,170,785,000 | 53,613,195 | 2,034,011,000 (2026-06-30) | 190,387,195 |
| Simon Property Group | 28,595,539,000 | 28,595,539,000 | 0 | 28,430,175,000 | 165,364,000 | 28,423,903,000 (2026-09-30) | 171,636,000 |
| Brixmor | 5,518,453,000 | 5,518,453,000 | 0 | 5,494,753,000 | 23,700,000 | 5,322,955,000 (2026-09-30) | 195,498,000 |
| Acadia Realty | 1,873,367,000 | 1,873,367,000 | 0 | 1,862,906,000 | 10,461,000 | 1,819,243,000 (2026-09-30) | 54,124,000 |
| Kite Realty | 3,027,937,000 | 3,027,937,000 | 0 | 3,025,478,000 | 2,459,000 | 2,807,320,000 (2026-09-30) | 220,617,000 |
| Vornado Realty Trust | n/a (incomplete) | not checked | n/a | 2,264,959,000 | n/a | 2,599,970,000 (2026-06-30) | n/a |
| Kilroy Realty | 3,250,442,000 (incomplete) | 4,625,442,000 | -1,375,000,000 | n/a | n/a | 2,238,508,000 (2015-12-31, STALE) | 1,011,934,000 |
| Highwoods Properties | 3,570,154,000 | not checked | n/a | n/a | n/a | n/a (tag not reported by filer) | n/a |
| Douglas Emmett | n/a (incomplete) | not checked | n/a | 5,548,870,000 | n/a | 5,729,491,000 (2026-09-30) | n/a |
| Hudson Pacific Properties | n/a (incomplete) | not checked | n/a | n/a | n/a | 2,623,835,000 (2018-12-31, STALE) | n/a |
| Brandywine Realty Trust | 2,563,948,000 | 2,563,948,000 | 0 | 2,556,862,000 | 7,086,000 | 2,409,562,000 (2026-09-30) | 154,386,000 |
| Regency Centers | 4,798,831,000 | not checked | n/a | 4,739,301,000 | 59,530,000 | 5,003,934,000 (2026-03-31, STALE) | -205,103,000 |
| Kimco Realty | n/a (incomplete) | not checked | n/a | 7,718,700,000 | n/a | 7,718,700,000 (2025-12-31, STALE) | n/a |
| Federal Realty | 4,963,602,000 | 4,963,602,000 | 0 | 4,963,602,000 | 0 | 4,963,602,000 (2025-12-31, STALE) | 0 |
| Macerich | n/a (incomplete) | not checked | n/a | 5,068,946,000 | n/a | 4,409,716,000 (2026-09-30) | n/a |
| Tanger | n/a (incomplete) | not checked | n/a | n/a | n/a | 1,663,654,000 (2026-09-30) | n/a |
| Phillips Edison | 2,401,665,000 | not checked | n/a | 2,375,328,000 | 26,337,000 | 2,521,454,000 (2026-09-30) | -119,789,000 |

Differences are expected (unamortized discounts and issuance costs, fair-value hedges, tag scope). Not forced to match.

## 5. Quotes verbatim (re-fetch and re-match), case-file names: SL Green, JBG Smith, Empire State Realty Trust

| claim | item | filed | exact re-extract | substring of fresh text | how | gap |
|---|---|---|---|---|---|---|
| SLG.ev10.1.01 | 1.01 | 2026-03-06 | yes | yes | re-fetched earlier (20261109T064835Z); compared with original fetch 20261109T012558Z from cache |  |
| JBGS.ev02.1.01 | 1.01 | 2026-08-28 | yes | yes | re-fetched earlier (20261109T064836Z); compared with original fetch 20261109T015707Z from cache |  |
| JBGS.ev03.2.03 | 2.03 | 2026-08-28 | yes | yes | re-fetched earlier (20261109T064836Z); compared with original fetch 20261109T015707Z from cache |  |
| ESRT.ev06.1.01 | 1.01 | 2026-07-17 | yes | yes | re-fetched earlier (20261109T064836Z); compared with original fetch 20261109T015709Z from cache |  |
| ESRT.ev07.2.03 | 2.03 | 2026-07-17 | yes | yes | re-fetched earlier (20261109T064836Z); compared with original fetch 20261109T015709Z from cache |  |
| ESRT.ev15.1.01 | 1.01 | 2026-04-15 | yes | yes | re-fetched earlier (20261109T064836Z); compared with original fetch 20261109T015709Z from cache |  |
| ESRT.ev16.2.03 | 2.03 | 2026-04-15 | yes | yes | re-fetched earlier (20261109T064836Z); compared with original fetch 20261109T015709Z from cache |  |

## 6. Override quotes: is each quote verbatim in the filing behind its claim_id?

| name | claim_id | quote found in filing text | filing |
|---|---|---|---|
| Office Properties Income Trust | OPI.ev10.1.03 | yes | https://www.sec.gov/Archives/edgar/data/1456772/000110465926076652/tm2618043d2_8k.htm |
| CBL & Associates | CBL.ev10.2.03 | yes | https://www.sec.gov/Archives/edgar/data/910612/000119312526139801/cbl-20260327.htm |
| SL Green | SLG.10q_2027_p0 | yes | https://www.sec.gov/Archives/edgar/data/1040971/000162828026071014/slg-20260930.htm |

## 7. 10-Q ladder: calendar-year mapping check

10-Q tags are read as: RemainderOfFiscalYear = rest of the current year, InNextTwelveMonths = next year, InYearTwo = the year after, and so on.
If that mapping is right, years with no refinancing activity carry the same principal in both filings. Raw values below ($), no pass/fail threshold.

| name | 10-Q period | year | 10-K value | 10-Q value | equal |
|---|---|---|---:|---:|---|
| SL Green | 2026-03-31 | 2027 | 2,569,277,000 | 1,236,390,000 | no |
| SL Green | 2026-03-31 | 2028 | 284,550,000 | 284,438,000 | no |
| SL Green | 2026-03-31 | 2029 | 177,000,000 | 189,200,000 | no |
| SL Green | 2026-03-31 | 2030 | 0 | 0 | yes |
| Cousins Properties | n/a | n/a | n/a | n/a | no 10-Q maturity facts after the 10-K ladder date (filer does not tag its 10-Q ladder) |
| JBG Smith | n/a | n/a | n/a | n/a | no 10-Q maturity facts after the 10-K ladder date (filer does not tag its 10-Q ladder) |
| Piedmont Office | n/a | n/a | n/a | n/a | no 10-Q maturity facts after the 10-K ladder date (filer does not tag its 10-Q ladder) |
| Office Properties Income Trust | n/a | n/a | n/a | n/a | no 10-Q maturity facts after the 10-K ladder date (filer does not tag its 10-Q ladder) |
| Empire State Realty Trust | 2026-06-30 | 2027 | 159,276,000 | 159,276,000 | yes |
| Empire State Realty Trust | 2026-06-30 | 2028 | 149,646,000 | 149,646,000 | yes |
| Empire State Realty Trust | 2026-06-30 | 2029 | 398,890,000 | 428,890,000 | no |
| Empire State Realty Trust | 2026-06-30 | 2030 | 513,111,000 | 333,111,000 | no |
| BXP | n/a | n/a | n/a | n/a | no 10-Q maturity facts after the 10-K ladder date (filer does not tag its 10-Q ladder) |
| CBL & Associates | 2026-06-30 | 2027 | 11,195 | 21,653,000 | no |
| CBL & Associates | 2026-06-30 | 2028 | 134,781,000 | 145,913,000 | no |
| CBL & Associates | 2026-06-30 | 2029 | 7,939,000 | 20,069,000 | no |
| CBL & Associates | 2026-06-30 | 2030 | 740,144,000 | 929,295,000 | no |
| Simon Property Group | n/a | n/a | n/a | n/a | no 10-Q maturity facts after the 10-K ladder date (filer does not tag its 10-Q ladder) |
| Brixmor | 2026-09-30 | 2027 | 400,000,000 | 400,000,000 | yes |
| Brixmor | 2026-09-30 | 2028 | 357,708,000 | 357,708,000 | yes |
| Brixmor | 2026-09-30 | 2029 | 753,203,000 | 753,203,000 | yes |
| Brixmor | 2026-09-30 | 2030 | 1,300,000,000 | 1,300,000,000 | yes |
| Acadia Realty | 2026-09-30 | 2027 | 309,638,000 | 106,029,000 | no |
| Acadia Realty | 2026-09-30 | 2028 | 845,235,000 | 143,384,000 | no |
| Acadia Realty | 2026-09-30 | 2029 | 98,292,000 | 182,891,000 | no |
| Acadia Realty | 2026-09-30 | 2030 | 326,850,000 | 589,173,000 | no |
| Kite Realty | n/a | n/a | n/a | n/a | no 10-Q maturity facts after the 10-K ladder date (filer does not tag its 10-Q ladder) |
| Vornado Realty Trust | n/a | n/a | n/a | n/a | no 10-Q maturity facts after the 10-K ladder date (filer does not tag its 10-Q ladder) |
| Kilroy Realty | n/a | n/a | n/a | n/a | no 10-Q maturity facts after the 10-K ladder date (filer does not tag its 10-Q ladder) |
| Highwoods Properties | n/a | n/a | n/a | n/a | no 10-Q maturity facts after the 10-K ladder date (filer does not tag its 10-Q ladder) |
| Douglas Emmett | n/a | n/a | n/a | n/a | no 10-Q maturity facts after the 10-K ladder date (filer does not tag its 10-Q ladder) |
| Hudson Pacific Properties | n/a | n/a | n/a | n/a | no 10-Q maturity facts after the 10-K ladder date (filer does not tag its 10-Q ladder) |
| Brandywine Realty Trust | 2026-09-30 | 2027 | 700,000,000 | 837,000,000 | no |
| Brandywine Realty Trust | 2026-09-30 | 2028 | 350,000,000 | 300,000,000 | no |
| Brandywine Realty Trust | 2026-09-30 | 2029 | 900,000,000 | 810,000,000 | no |
| Brandywine Realty Trust | 2026-09-30 | 2030 | 0 | 0 | yes |
| Regency Centers | 2026-03-31 | 2027 | 757,609,000 | 757,609,000 | yes |
| Regency Centers | 2026-03-31 | 2028 | 480,304,000 | 390,304,000 | no |
| Regency Centers | 2026-03-31 | 2029 | 527,739,000 | 527,739,000 | yes |
| Regency Centers | 2026-03-31 | 2030 | 607,608,000 | 607,608,000 | yes |
| Kimco Realty | n/a | n/a | n/a | n/a | no 10-Q maturity facts after the 10-K ladder date (filer does not tag its 10-Q ladder) |
| Federal Realty | n/a | n/a | n/a | n/a | no 10-Q maturity facts after the 10-K ladder date (filer does not tag its 10-Q ladder) |
| Macerich | n/a | n/a | n/a | n/a | no 10-Q maturity facts after the 10-K ladder date (filer does not tag its 10-Q ladder) |
| Tanger | n/a | n/a | n/a | n/a | no 10-Q maturity facts after the 10-K ladder date (filer does not tag its 10-Q ladder) |
| Phillips Edison | n/a | n/a | n/a | n/a | no 10-Q maturity facts after the 10-K ladder date (filer does not tag its 10-Q ladder) |

**11 of 28 overlapping year values are equal.** Unequal values are expected where debt was refinanced, repaid or drawn after year-end.

## Conflicts and gaps

- CONFLICT CBL & Associates / LongTermDebtMaturitiesRepaymentsOfPrincipalInYearTwo: kept 11195.0, others 11,195,000. filer tagged scale differs from the rest of its own 10-K table; kept as tagged
- RESOLVED (plumbing: period-selection) Tanger / LongTermDebt: raw row before the fix: A=n/a (no 10-K instant at 2025-12-31) vs B=1,596,821,000 (0001628280-26-071352). Evidence: companyfacts holds this 2025-12-31 value only as a comparative in 10-Q filings (10-Q 0001628280-26-071352 is the latest), and the frames API takes the latest filing for the instant. Fix: side A now applies the same rule; the values agree.
- FALLBACK SL Green / latest_cash: STALE: latest value is 223 days old at as_of; no newer filing tagged (end 2026-03-31). Action: older value kept and flagged, not replaced.
- FALLBACK SL Green / latest_debt: STALE: latest value is 1409 days old at as_of; no newer filing tagged (end 2022-12-31). Action: older value kept and flagged, not replaced.
- GAP JBG Smith / after_2030: no 10-K fact with end 2025-12-31. Action: left as missing.
- FALLBACK JBG Smith / latest_debt: STALE: latest value is 3419 days old at as_of; no newer filing tagged (end 2017-06-30). Action: older value kept and flagged, not replaced.
- GAP Office Properties Income Trust / price: partial window: 99 closes since 2026-06-18 (141 days); 52-week drawdown not computable. Since-first-close drawdown 61.6% shown as context only. Market view not scored; name left out of the sector median.
- FALLBACK Empire State Realty Trust / latest_debt: STALE: latest value is 2597 days old at as_of; no newer filing tagged (end 2019-09-30). Action: older value kept and flagged, not replaced.
- GAP BXP / y1_2026: no 10-K fact with end 2025-12-31. Action: left as missing.
- GAP BXP / y2_2027: no 10-K fact with end 2025-12-31. Action: left as missing.
- GAP BXP / y3_2028: no 10-K fact with end 2025-12-31. Action: left as missing.
- GAP BXP / y4_2029: no 10-K fact with end 2025-12-31. Action: left as missing.
- GAP BXP / y5_2030: no 10-K fact with end 2025-12-31. Action: left as missing.
- GAP BXP / after_2030: no 10-K fact with end 2025-12-31. Action: left as missing.
- FALLBACK BXP / latest_debt: STALE: latest value is 1774 days old at as_of; no newer filing tagged (end 2021-12-31). Action: older value kept and flagged, not replaced.
- GAP Vornado Realty Trust / y1_2026: tag not reported by filer. Action: left as missing.
- GAP Vornado Realty Trust / y2_2027: tag not reported by filer. Action: left as missing.
- GAP Vornado Realty Trust / y3_2028: tag not reported by filer. Action: left as missing.
- GAP Vornado Realty Trust / y4_2029: tag not reported by filer. Action: left as missing.
- GAP Vornado Realty Trust / y5_2030: tag not reported by filer. Action: left as missing.
- GAP Vornado Realty Trust / after_2030: tag not reported by filer. Action: left as missing.
- GAP Kilroy Realty / y3_2028: tag not reported by filer. Action: left as missing.
- GAP Kilroy Realty / y4_2029: tag not reported by filer. Action: left as missing.
- GAP Kilroy Realty / y5_2030: tag not reported by filer. Action: left as missing.
- FALLBACK Kilroy Realty / latest_cash: STALE: latest value is 223 days old at as_of; no newer filing tagged (end 2026-03-31). Action: older value kept and flagged, not replaced.
- FALLBACK Kilroy Realty / latest_debt: STALE: latest value is 3966 days old at as_of; no newer filing tagged (end 2015-12-31). Action: older value kept and flagged, not replaced.
- FALLBACK Highwoods Properties / latest_cash: STALE: latest value is 223 days old at as_of; no newer filing tagged (end 2026-03-31). Action: older value kept and flagged, not replaced.
- GAP Highwoods Properties / latest_debt: tag not reported by filer. Action: left as missing.
- GAP Douglas Emmett / y1_2026: no 10-K fact with end 2025-12-31; filer reports related maturity tags (not used): us-gaap:LongTermDebtMaturitiesRepaymentsOfPrincipalInNextRollingTwelveMonths, us-gaap:LongTermDebtMaturitiesRepaymentsOfPrincipalInRollingAfterYearFive, us-gaap:LongTermDebtMaturitiesRepaymentsOfPrincipalInRollingYearFive, us-gaap:LongTermDebtMaturitiesRepaymentsOfPrincipalInRollingYearFour, us-gaap:LongTermDebtMaturitiesRepaymentsOfPrincipalInRollingYearThree, us-gaap:LongTermDebtMaturitiesRepaymentsOfPrincipalInRollingYearTwo. Action: left as missing.
- GAP Douglas Emmett / y2_2027: no 10-K fact with end 2025-12-31; filer reports related maturity tags (not used): us-gaap:LongTermDebtMaturitiesRepaymentsOfPrincipalInNextRollingTwelveMonths, us-gaap:LongTermDebtMaturitiesRepaymentsOfPrincipalInRollingAfterYearFive, us-gaap:LongTermDebtMaturitiesRepaymentsOfPrincipalInRollingYearFive, us-gaap:LongTermDebtMaturitiesRepaymentsOfPrincipalInRollingYearFour, us-gaap:LongTermDebtMaturitiesRepaymentsOfPrincipalInRollingYearThree, us-gaap:LongTermDebtMaturitiesRepaymentsOfPrincipalInRollingYearTwo. Action: left as missing.
- GAP Douglas Emmett / y3_2028: no 10-K fact with end 2025-12-31; filer reports related maturity tags (not used): us-gaap:LongTermDebtMaturitiesRepaymentsOfPrincipalInNextRollingTwelveMonths, us-gaap:LongTermDebtMaturitiesRepaymentsOfPrincipalInRollingAfterYearFive, us-gaap:LongTermDebtMaturitiesRepaymentsOfPrincipalInRollingYearFive, us-gaap:LongTermDebtMaturitiesRepaymentsOfPrincipalInRollingYearFour, us-gaap:LongTermDebtMaturitiesRepaymentsOfPrincipalInRollingYearThree, us-gaap:LongTermDebtMaturitiesRepaymentsOfPrincipalInRollingYearTwo. Action: left as missing.
- GAP Douglas Emmett / y4_2029: no 10-K fact with end 2025-12-31; filer reports related maturity tags (not used): us-gaap:LongTermDebtMaturitiesRepaymentsOfPrincipalInNextRollingTwelveMonths, us-gaap:LongTermDebtMaturitiesRepaymentsOfPrincipalInRollingAfterYearFive, us-gaap:LongTermDebtMaturitiesRepaymentsOfPrincipalInRollingYearFive, us-gaap:LongTermDebtMaturitiesRepaymentsOfPrincipalInRollingYearFour, us-gaap:LongTermDebtMaturitiesRepaymentsOfPrincipalInRollingYearThree, us-gaap:LongTermDebtMaturitiesRepaymentsOfPrincipalInRollingYearTwo. Action: left as missing.
- GAP Douglas Emmett / y5_2030: no 10-K fact with end 2025-12-31; filer reports related maturity tags (not used): us-gaap:LongTermDebtMaturitiesRepaymentsOfPrincipalInNextRollingTwelveMonths, us-gaap:LongTermDebtMaturitiesRepaymentsOfPrincipalInRollingAfterYearFive, us-gaap:LongTermDebtMaturitiesRepaymentsOfPrincipalInRollingYearFive, us-gaap:LongTermDebtMaturitiesRepaymentsOfPrincipalInRollingYearFour, us-gaap:LongTermDebtMaturitiesRepaymentsOfPrincipalInRollingYearThree, us-gaap:LongTermDebtMaturitiesRepaymentsOfPrincipalInRollingYearTwo. Action: left as missing.
- GAP Douglas Emmett / after_2030: no 10-K fact with end 2025-12-31; filer reports related maturity tags (not used): us-gaap:LongTermDebtMaturitiesRepaymentsOfPrincipalInNextRollingTwelveMonths, us-gaap:LongTermDebtMaturitiesRepaymentsOfPrincipalInRollingAfterYearFive, us-gaap:LongTermDebtMaturitiesRepaymentsOfPrincipalInRollingYearFive, us-gaap:LongTermDebtMaturitiesRepaymentsOfPrincipalInRollingYearFour, us-gaap:LongTermDebtMaturitiesRepaymentsOfPrincipalInRollingYearThree, us-gaap:LongTermDebtMaturitiesRepaymentsOfPrincipalInRollingYearTwo. Action: left as missing.
- GAP Hudson Pacific Properties / y1_2026: no 10-K fact with end 2025-12-31. Action: left as missing.
- GAP Hudson Pacific Properties / y2_2027: no 10-K fact with end 2025-12-31. Action: left as missing.
- GAP Hudson Pacific Properties / y3_2028: no 10-K fact with end 2025-12-31. Action: left as missing.
- GAP Hudson Pacific Properties / y4_2029: no 10-K fact with end 2025-12-31. Action: left as missing.
- GAP Hudson Pacific Properties / y5_2030: no 10-K fact with end 2025-12-31. Action: left as missing.
- GAP Hudson Pacific Properties / after_2030: no 10-K fact with end 2025-12-31. Action: left as missing.
- FALLBACK Hudson Pacific Properties / latest_cash: STALE: latest value is 223 days old at as_of; no newer filing tagged (end 2026-03-31). Action: older value kept and flagged, not replaced.
- FALLBACK Hudson Pacific Properties / latest_debt: STALE: latest value is 2870 days old at as_of; no newer filing tagged (end 2018-12-31). Action: older value kept and flagged, not replaced.
- FALLBACK Regency Centers / latest_cash: STALE: latest value is 3510 days old at as_of; no newer filing tagged (end 2017-03-31). Action: older value kept and flagged, not replaced.
- FALLBACK Regency Centers / latest_debt: STALE: latest value is 223 days old at as_of; no newer filing tagged (end 2026-03-31). Action: older value kept and flagged, not replaced.
- GAP Kimco Realty / y1_2026: no 10-K fact with end 2025-12-31. Action: left as missing.
- GAP Kimco Realty / y2_2027: no 10-K fact with end 2025-12-31. Action: left as missing.
- GAP Kimco Realty / y3_2028: no 10-K fact with end 2025-12-31. Action: left as missing.
- GAP Kimco Realty / y4_2029: no 10-K fact with end 2025-12-31. Action: left as missing.
- GAP Kimco Realty / y5_2030: no 10-K fact with end 2025-12-31. Action: left as missing.
- GAP Kimco Realty / after_2030: no 10-K fact with end 2025-12-31. Action: left as missing.
- FALLBACK Kimco Realty / latest_debt: STALE: latest value is 313 days old at as_of; no newer filing tagged (end 2025-12-31). Action: older value kept and flagged, not replaced.
- FALLBACK Federal Realty / latest_cash: STALE: latest value is 223 days old at as_of; no newer filing tagged (end 2026-03-31). Action: older value kept and flagged, not replaced.
- FALLBACK Federal Realty / latest_debt: STALE: latest value is 313 days old at as_of; no newer filing tagged (end 2025-12-31). Action: older value kept and flagged, not replaced.
- GAP Macerich / y1_2026: tag not reported by filer. Action: left as missing.
- GAP Macerich / y2_2027: tag not reported by filer. Action: left as missing.
- GAP Macerich / y3_2028: tag not reported by filer. Action: left as missing.
- GAP Macerich / y4_2029: tag not reported by filer. Action: left as missing.
- GAP Macerich / y5_2030: tag not reported by filer. Action: left as missing.
- GAP Macerich / after_2030: tag not reported by filer. Action: left as missing.
- GAP Tanger / y1_2026: tag not reported by filer. Action: left as missing.
- GAP Tanger / y2_2027: tag not reported by filer. Action: left as missing.
- GAP Tanger / y3_2028: tag not reported by filer. Action: left as missing.
- GAP Tanger / y4_2029: tag not reported by filer. Action: left as missing.
- GAP Tanger / y5_2030: tag not reported by filer. Action: left as missing.
- GAP Tanger / after_2030: tag not reported by filer. Action: left as missing.
