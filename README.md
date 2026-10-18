# CS200: Data Structures & Algorithms — Project 1
## Restaurant & Bar Owners Analytics Desktop Application

An advanced, production-grade desktop application engineered for university Data Structures & Algorithms coursework (CS200, Project 1). 

Built strictly with Python 3.10+, PyQt6, SQLite, and custom-instrumented algorithmic routines. **Zero built-in sorting or searching shortcuts (`sort()`, `sorted()`, `heapq`, `bisect`, or Python `dict` lookups) are used for the graded DSA requirements.** Every algorithm is implemented manually from fundamental principles.

---

## 📋 Table of Contents
1. [Architecture & Project Structure](#architecture--project-structure)
2. [Domain Entity Specification](#domain-entity-specification)
3. [Algorithm Complexity & Stability Matrix](#algorithm-complexity--stability-matrix)
4. [Key System Features](#key-system-features)
5. [Setup & Installation Instructions](#setup--installation-instructions)
6. [Running the Application](#running-the-application)
7. [Running Tests](#running-tests)
8. [Instructor Demonstration Script](#instructor-demonstration-script)
9. [Feature Checklist & Compliance](#feature-checklist--compliance)

---

## 🏛 Architecture & Project Structure

The project strictly separates UI logic, background workers, persistent storage, and core algorithmic procedures:

```
project/
│
├── main.py                     # Application entry point (PyQt6 event loop & styling)
├── demo_cli.py                 # Automated end-to-end CLI demonstration for grading
├── requirements.txt            # Python dependencies (PyQt6, requests, bs4, matplotlib, pytest)
├── README.md                   # Complete architectural guide & complexity documentation
├── restaurants.db              # SQLite persistence database (auto-created on startup)
│
├── ui/                         # Presentation Layer (PyQt6)
│   ├── __init__.py
│   ├── main_window.py          # Unified MainWindow with QTabWidget & global menu/status bar
│   ├── scrape_tab.py           # Scraping controls: Start, Pause, Resume, Stop & Bonus URL Scraper
│   ├── data_tab.py             # Virtualized QTableView, per-column sorting, search & metrics
│   ├── benchmark_dialog.py     # Comprehensive 12-algorithm benchmark suite & Matplotlib chart
│   ├── filter_builder.py       # Visual Composite Filter Expression Tree Builder (And/Or/Not)
│   └── multilevel_sort_dialog.py # Hierarchical multi-key sorter with stability guard
│
├── scraper/                    # Ingestion & Asynchronous Workers Layer
│   ├── __init__.py
│   ├── overpass_scraper.py     # OpenStreetMap Overpass API client with failover & chunking
│   ├── url_scraper.py          # BONUS: Web scraper (schema.org JSON-LD, Microdata, Heuristics)
│   └── worker.py               # QThread workers (ScrapeWorker, UrlScrapeWorker, SortWorker, BenchmarkWorker)
│
├── algorithms/                 # Pure Manual Algorithmic Implementations (Zero Built-ins)
│   ├── __init__.py
│   ├── metrics.py              # Thread-safe SortMetrics & SearchMetrics counter objects
│   ├── sorting.py              # 12 Hand-crafted sorting algorithms with move/swap instrumentation
│   └── searching.py            # 6 Hand-crafted searching algorithms & manual chaining Hash Table
│
├── core/                       # Domain Models, Virtualization & Storage Layer
│   ├── __init__.py
│   ├── models.py               # Restaurant entity (10 required attributes + extra numeric columns)
│   ├── storage.py              # SQLite batch persistence & CSV import/export manager
│   ├── table_model.py          # QAbstractTableModel backing smooth virtualized 15,000+ row rendering
│   └── filters.py              # Composite boolean expression tree (AndNode, OrNode, NotNode, ConditionNode)
│
└── tests/                      # Automated Unit Testing Suite
    ├── __init__.py
    └── test_algorithms.py      # 108 pytest test cases (edge cases, stability, ranges, filters)
```

---

## 🍽 Domain Entity Specification

The entity models **Restaurant and Bar Owners** across worldwide regions, containing all 10 required attributes plus secondary numeric columns for multi-level and numeric sorting:

| # | Attribute Key | Data Type | Description | Fallback / Behavior |
|---|---------------|-----------|-------------|---------------------|
| 1 | `id` | `int` | Unique OpenStreetMap Element or Hash ID | Generated or parsed |
| 2 | `owner` | `str` | Owner / Operator Name | Brand name or `"Unknown (Owner not listed)"` |
| 3 | `name` | `str` | Business Venue Name | Tagged name or fallback |
| 4 | `business_type` | `str` | Type: restaurant / bar / pub / cafe / fast_food | Canonical amenity |
| 5 | `cuisine` | `str` | Cuisine Style (e.g. Italian, Pakistani, Burger) | `"Unspecified"` |
| 6 | `city` | `str` | City | Query region fallback |
| 7 | `country` | `str` | Country | Query region fallback |
| 8 | `phone` | `str` | Contact Phone Number | `"N/A"` |
| 9 | `website` | `str` | Website URL | `"N/A"` |
| 10 | `opening_year` | `int` | Founding / Opening Year (Numeric 1) | Parsed from date or pseudo-random |
| 11 | `rating` | `float` | Customer Rating from 1.0 to 5.0 (Numeric 2) | Formatted with `★` symbol |
| 12 | `seats` | `int` | Seating Capacity (Numeric 3) | Formatted as `N seats` |

---

## 📊 Algorithm Complexity & Stability Matrix

All algorithms are implemented **purely by hand** without using Python's `sort()`, `sorted()`, `heapq`, `bisect`, or built-in dictionary lookups for search demonstration.

### Sorting Algorithms (12 Total)
| Algorithm | Best Time | Average Time | Worst Time | Space | Stable? | Key Characteristic |
|-----------|-----------|--------------|------------|-------|---------|---------------------|
| **Bubble Sort** | $O(n)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | **Yes** | Early exit when no swaps occur on a pass. |
| **Selection Sort** | $O(n^2)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | **No** | Repeatedly selects minimum from unsorted portion. |
| **Insertion Sort** | $O(n)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | **Yes** | Inserts elements into pre-sorted prefix. Fast on nearly sorted data. |
| **Merge Sort** | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(n)$ | **Yes** | Bottom-up iterative merge. Guaranteed $O(n \log n)$, ideal for multi-level sort. |
| **Quick Sort** | $O(n \log n)$ | $O(n \log n)$ | $O(n^2)$ | $O(\log n)$ | **No** | Median-of-three pivot; iterative stack prevents recursion depth overflow. |
| **Heap Sort** | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(1)$ | **No** | In-place binary max-heap construction and root extraction. |
| **Shell Sort** | $O(n \log n)$ | $O(n^{4/3})$ | $O(n^2)$ | $O(1)$ | **No** | Ciura gap sequence; swaps far-apart elements. |
| **Counting Sort** | $O(n + k)$ | $O(n + k)$ | $O(n + k)$ | $O(n + k)$ | **Yes** | Frequency histogram; stable backwards accumulation (integers only). |
| **Radix Sort** | $O(d(n + k))$ | $O(d(n + k))$ | $O(d(n + k))$ | $O(n + k)$ | **Yes** | Least Significant Digit (LSD) with 10 buckets (integers only). |
| **Tim Sort** | $O(n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(n)$ | **Yes** | Minirun detection, binary insertion sort, and stack merge invariants. |
| **Cocktail Shaker Sort** | $O(n)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | **Yes** | Bidirectional bubble sort traversing alternating directions. |
| **Comb Sort** | $O(n \log n)$ | $O(n^2 / 2^p)$ | $O(n^2)$ | $O(1)$ | **No** | Bubble sort variant with 1.3 shrink factor and Rule of 11. |

> **Swap & Move Definition:** For in-place comparison algorithms (Bubble, Selection, Quick, Heap, Cocktail, Comb), a swap represents an exchange `arr[i], arr[j] = arr[j], arr[i]`. For Merge Sort and Insertion Sort, each element move/write into a destination index is counted as a move/swap and documented in the metrics.

---

### Searching Algorithms (6 Total)
| Algorithm | Best Time | Average Time | Worst Time | Space | Requirements / Preconditions |
|-----------|-----------|--------------|------------|-------|------------------------------|
| **Linear Search** | $O(1)$ | $O(n)$ | $O(n)$ | $O(1)$ | None (works on unsorted data). |
| **Binary Search** | $O(1)$ | $O(\log n)$ | $O(\log n)$ | $O(1)$ | **Requires sorted data**. Auto-sorts with notification if unsorted. Returns **all duplicate matches**. |
| **Jump Search** | $O(1)$ | $O(\sqrt{n})$ | $O(\sqrt{n})$ | $O(1)$ | **Requires sorted data**. Jumps in blocks of $\lfloor \sqrt{n} \rfloor$. Returns **all duplicate matches**. |
| **Interpolation Search** | $O(1)$ | $O(\log \log n)$ | $O(n)$ | $O(1)$ | **Requires sorted numeric data** with uniform distribution. Probes position numerically. |
| **Exponential Search** | $O(1)$ | $O(\log n)$ | $O(\log n)$ | $O(1)$ | **Requires sorted data**. Doubles indices $1, 2, 4, 8\dots$, then binary searches range. |
| **Hash-based Lookup** | $O(1)$ | $O(1)$ | $O(n)$ | $O(n)$ | Builds custom **separate-chaining hash table** (Bernstein djb2 hash, prime capacity). |

---

## ⚡ Key System Features

### 1. Robust Scraping Engine (15,000+ Entities)
- Queries OpenStreetMap Overpass API in chunked bounding boxes across London, Paris, Berlin, Rome, Madrid, New York, Lahore, Tokyo, Toronto, Sydney, Vienna, and Karachi.
- **Failover Mirrors:** Automatically switches between `overpass-api.de`, `overpass.kumi.systems`, and `maps.mail.ru`.
- **High-Throughput Mode:** Toggleable realistic synthetic generator to swiftly reach 15,000 entities in seconds without waiting for public Overpass rate limits.
- **Cooperative Controls:** Full **START**, **PAUSE**, **RESUME**, and **STOP** buttons via `threading.Event` and cooperative flags. STOP retains all scraped data.
- **Batch Persistence:** Periodically commits batches to SQLite (`INSERT OR REPLACE`) so data survives restarts.

### 2. Bonus Web URL Scraper
- User pastes an arbitrary restaurant/bar URL.
- Extracts attributes using:
  1. **schema.org JSON-LD:** `<script type="application/ld+json">` parsing `@type` `Restaurant`, `BarOrPub`, `CafeOrCoffeeShop`, etc.
  2. **HTML5 Microdata:** `[itemscope][itemtype*="Restaurant"]` extraction.
  3. **Heuristic Fallback:** Extracts OpenGraph headers, `<title>`, `tel:` links, and address text.
- Validates URL syntax, catches HTTP/timeout errors, and presents clear `QMessageBox` alerts.

### 3. Virtualized UI Performance (15,000+ Rows)
- Implements `QAbstractTableModel` paired with `QTableView`.
- Never loads 15,000 widgets into memory; renders only the viewport rows on-demand.
- Sorting runs in a background `QThread` with cancellation support and progress indication.

### 4. Multi-Level Hierarchical Sorting
- Allows chaining multiple keys (e.g. `Country ASC` $\rightarrow$ `City ASC` $\rightarrow$ `Rating DESC`).
- Reorder levels via Move Up / Move Down buttons.
- **Stability Guard:** Enforces multi-pass sorting from least significant key to most significant key. If the user selects an unstable algorithm (e.g. Quick Sort or Heap Sort), the system displays a clear warning modal.

### 5. Composite Filter Expression Tree
- Expression tree supporting `ConditionNode`, `AndNode`, `OrNode`, and `NotNode`.
- Visual dialog generates real-time human-readable boolean expressions:
  `((City equals 'Lahore' AND Type equals 'bar') OR NOT (Rating < 3.5))`
- Supports numeric range filtering (`between`) and string matching (`contains`, `starts_with`, `regex`, case sensitivity toggle).

### 6. Interactive Benchmark Suite
- Concurrently benchmarks all 12 sorting algorithms on fresh copies of the selected column.
- Highlights the fastest algorithm in green with a badge.
- Features a sample-size limiter for $O(n^2)$ sorts on huge datasets.
- Renders an **embedded Matplotlib bar chart** comparing execution speeds side-by-side.
- Exports benchmark comparison metrics to CSV.

---

## 🚀 Setup & Installation Instructions

### Prerequisites
- Python 3.10, 3.11, or 3.12
- Windows, macOS, or Linux

### 1. Clone or Open Project
```powershell
cd "f:\University of Engineering & Technology\Semester 3\DSA - Lab\Project 1 alpha"
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

---

## 🖥 Running the Application

Launch the full PyQt6 desktop GUI:
```powershell
python main.py
```

---

## 🧪 Running Tests

The test suite covers all 12 sorting algorithms across all edge cases (empty, single element, duplicates, pre-sorted, reversed, random vs Python built-in, stability preservation), all 6 searching algorithms (verifying that range searches return all duplicate matches), and composite expression trees.

Execute pytest with verbose output:
```powershell
pytest tests/test_algorithms.py -v
```

Expected Output:
```
============================= 108 passed in 0.68s =============================
```

---

## 🎬 Instructor Demonstration Script

To present each requirement to the instructor or grading panel in an automated, interactive terminal demonstration, execute:
```powershell
python demo_cli.py
```

This sequentially showcases:
1. **Scraping & Storage:** Ingesting 15,000 entities into SQLite.
2. **Pause / Resume:** Demonstrating thread-safe suspension and continuation.
3. **12 Sorting Algorithms:** Running all 12 algorithms with comparisons, moves, and times.
4. **Benchmark Suite:** Comparing all 12 sorts and announcing the fastest.
5. **Multi-Level Hierarchical Sort:** 3-tier sort with stability preservation.
6. **Searching:** Range retrieval of all 143 duplicate matches across Linear, Binary, Jump, Interpolation, Exponential, and Hash Table.
7. **Composite Expression Tree:** Evaluating `(City = 'Lahore' AND Type = 'bar') OR NOT (Rating < 3.5)`.
8. **Bonus Web URL Scraper:** Parsing web pages with JSON-LD / Microdata.

---

## ✅ Feature Checklist & Compliance

| # | Requirement | Status | Implementation Details |
|---|-------------|:------:|------------------------|
| **1** | **Entity Attributes (10 Required)** | ✅ Complete | ID, Owner, Name, Type, Cuisine, City, Country, Phone, Website, Opening Year, Rating, Seats in `core/models.py`. |
| **2** | **Scraping Engine (15,000+ Entities)** | ✅ Complete | Overpass OSM chunking with failover endpoints and fast synthesizer in `scraper/overpass_scraper.py`. |
| **3** | **Start / Pause / Resume / Stop Controls** | ✅ Complete | Thread-safe `threading.Event` controls in `scraper/worker.py` and `ui/scrape_tab.py`. STOP retains all data. |
| **4** | **Real-time Throughput & Progress Bar** | ✅ Complete | Shows entities scraped / target, entities-per-second, and live console in `ui/scrape_tab.py`. |
| **5** | **SQLite Persistence & CSV Export/Import** | ✅ Complete | Batch `executemany` insertion, startup reload, CSV import/export in `core/storage.py`. |
| **6** | **BONUS: Web URL Scraper** | ✅ Complete | schema.org JSON-LD, Microdata, and heuristic fallback in `scraper/url_scraper.py`. |
| **7** | **Virtualized Main List Page** | ✅ Complete | `QAbstractTableModel` + `QTableView` rendering 15,000+ items smoothly in `core/table_model.py` & `ui/data_tab.py`. |
| **8** | **12 Hand-crafted Sorting Algorithms** | ✅ Complete | Bubble, Selection, Insertion, Merge, Quick (median-of-three iterative), Heap, Shell, Counting, Radix, TimSort, Cocktail Shaker, Comb in `algorithms/sorting.py`. **Zero built-ins**. |
| **9** | **Sorting Instrumentation** | ✅ Complete | Non-global `SortMetrics` measuring exact comparisons, moves/swaps, time in ms, complexity, and stability. |
| **10** | **Asynchronous Worker with Cancel** | ✅ Complete | `SortWorker` running in background `QThread` with cooperative cancellation and progress in `scraper/worker.py`. |
| **11** | **Benchmark Suite & Chart** | ✅ Complete | Runs all 12 sorts, highlights fastest, sample limiter for $O(n^2)$, embedded Matplotlib chart, CSV export in `ui/benchmark_dialog.py`. |
| **12** | **Sort Scope (Full vs Filtered)** | ✅ Complete | Radio toggle for "Full dataset" vs "Currently filtered results" in `ui/data_tab.py`. |
| **13** | **Multi-Level Hierarchical Sorting** | ✅ Complete | Multi-pass stable sorting with level reordering and stability warnings in `ui/multilevel_sort_dialog.py`. |
| **14** | **6 Hand-crafted Search Algorithms** | ✅ Complete | Linear, Binary (range), Jump (range), Interpolation (numeric), Exponential (range), and Chaining Hash Table in `algorithms/searching.py`. |
| **15** | **Composite Filter Builder Tree** | ✅ Complete | Expression tree (`And`, `Or`, `Not`, `Condition`) with live visual preview in `core/filters.py` and `ui/filter_builder.py`. |
| **16** | **Comprehensive Unit Tests** | ✅ Complete | 108 pytest unit tests passing in under 1 second in `tests/test_algorithms.py`. |
"# DSA-Project1" 
