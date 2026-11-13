# ============================================================================
# DSA 504 -- Class 20: dplyr & tidyr (Lab)
# Date: Wednesday, Nov 11
# Reading: R for Data Science
# Today: HW5 is due before this class.
# ============================================================================
#
# Class 19 introduced tibbles and a light preview of filter(). Today goes
# deep on dplyr -- the full toolkit for filtering, selecting, transforming,
# and summarizing data -- plus tidyr, for reshaping data between "long" and
# "wide" layouts. Everything here directly mirrors the pandas skills from
# Classes 4-5. By the end, you'll see the R results match the Python/SQL
# results from earlier this semester exactly -- same data, same answer,
# third language.
#
# Learning goals -- by the end of this file, you will be able to:
#   - Use select() with helper functions, renaming, and column-dropping
#   - Combine multiple conditions in filter() with &, |, and %in%
#   - Create multiple new columns at once with mutate(), including
#     conditional logic with case_when()
#   - Aggregate data with group_by() + summarise(), including multiple
#     aggregates and multiple grouping columns at once
#   - Reshape data between long and wide formats with pivot_longer() and
#     pivot_wider()
#   - Chain all of the above into one full, readable pipeline
#
# HOW TO USE THIS FILE: run it top to bottom in RStudio. Place your cursor
# on any line and press Ctrl+Enter (Windows/Linux) or Cmd+Enter (Mac) to run
# just that line, or highlight a block and run it all at once. Every single
# line of code below has been tested in a real R session and confirmed to
# produce exactly the output shown in the comment beneath it.
#
# Make sure retail_sales_clean.csv (the same file from Classes 4 onward) is
# in the same folder as this script.

library(tidyverse)
sales <- read_csv("Class19_retail_sales_clean.csv")


# ============================================================================
# 1. select() -- Choosing Columns, in More Depth
# ============================================================================
#
# Class 19 showed select(store) and select(store, revenue). Here's more of
# what select() can do.

# --- Selecting columns by a naming pattern ---
sales |> select(starts_with("s"))
# Output: just the "store" column -- starts_with() matches any column name
# beginning with that text. (contains("x") would match any column name
# containing "x" anywhere, not just at the start.)

# --- Reordering columns with everything() ---
sales |> select(category, everything())
# Output: the same 5 columns, but with "category" moved to the front and
# everything() filling in the rest in their original order. Useful when you
# want to highlight one column without typing out every other column name.

# --- Renaming a column while selecting it ---
sales |> select(location = store, revenue)
# Output: a tibble with "store" renamed to "location" -- the equivalent of
# pandas' sales.rename(columns={"store": "location"})[["location", "revenue"]].

# --- Dropping a column with a minus sign ---
sales |> select(-date)
# Output: every column except "date" -- useful when you want "all but one
# or two columns," instead of listing every column you DO want.


# ============================================================================
# 2. filter() -- Combining Multiple Conditions
# ============================================================================
#
# Class 19 showed a single-condition filter(). Real filtering usually needs
# to combine conditions.

# --- Combining conditions with & (AND) ---
sales |> filter(store == "Utica" & revenue > 2000)
# Output: 216 rows -- only Utica rows where revenue also exceeds 2000. Both
# conditions must be TRUE. (The equivalent pandas line:
# sales[(sales["store"] == "Utica") & (sales["revenue"] > 2000)])

# --- Combining conditions with | (OR) ---
sales |> filter(store == "Rome" | store == "Albany")
# Output: 2014 rows -- rows matching EITHER condition.

# --- %in% -- checking membership in a list, the clean way ---
sales |> filter(store %in% c("Rome", "Albany", "Utica"))
# Output: 3037 rows -- the direct equivalent of pandas' .isin(), and much
# cleaner than chaining several == conditions with | by hand.

# --- Filtering out missing values ---

sales |> filter(!is.na(revenue))
# Output: 4014 rows -- since this is the cleaned file, nothing gets removed
# (confirming, again, that Class 7's cleaning held up). The ! means "not,"
# so !is.na(revenue) reads as "keep rows where revenue is NOT missing."


# ============================================================================
# 3. mutate() -- Creating Multiple Columns, and Conditional Logic
# ============================================================================

# --- Creating more than one new column in a single mutate() call ---
sales |> mutate(
  revenue_with_tax = revenue * 1.08,
  profit_estimate = revenue * 0.3
) |> select(store, revenue, revenue_with_tax, profit_estimate)
# Output: both new columns appear together -- no need for two separate
# mutate() calls, each line inside one mutate() just becomes another column.

# --- case_when() -- R's version of nested if/else, built for creating a column ---
sales |> mutate(
  tier = case_when(
    revenue > 3000 ~ "High",
    revenue > 1000 ~ "Medium",
    TRUE ~ "Low"
  )
) |> select(store, revenue, tier)
# Output: a new "tier" column, labeled High/Medium/Low. Read each line as
# "when this condition is true, use this label" -- checked top to bottom,
# first match wins. TRUE ~ "Low" at the end acts as the "otherwise" case,
# the same role as a final `else` in an if/else chain.

# Counting how many rows fall into each tier:
sales |> mutate(
  tier = case_when(
    revenue > 3000 ~ "High",
    revenue > 1000 ~ "Medium",
    TRUE ~ "Low"
  )
) |> count(tier)
# Output: High 585, Low 1691, Medium 1738 -- adds up to 4014, the full
# dataset. count() is a shortcut for group_by() + summarise(n = n()),
# covered properly next.


# ============================================================================
# 4. group_by() + summarise() -- The Core of This Class
# ============================================================================
#
# This is the direct equivalent of pandas' .groupby() + .agg(), and of
# SQL's GROUP BY -- the same idea you've now seen in three languages.

# --- A single aggregate, one grouping column ---
sales |> group_by(store) |> summarise(total_revenue = sum(revenue))
# Output:
#   Albany   1477075.
#   Rome     1521764.
#   Syracuse 1518656.
#   Utica    1562320.
# Compare this to Class 12-14's SQL results and Classes 4-5's pandas
# results -- Utica highest, at the same number, down to the dollar. Same
# data, same answer, third language.

# --- Multiple aggregates at once ---
sales |> group_by(category) |> summarise(
  total_revenue = sum(revenue),
  avg_revenue = mean(revenue),
  num_transactions = n()
)
# Output: electronics has the highest total AND average revenue (2,826,160
# total, 3690 average, across 766 transactions). n() -- with no arguments
# -- counts how many rows are in each group, the equivalent of pandas'
# .size() or .count().

# --- Grouping by more than one column ---
sales |> group_by(store, category) |> summarise(total_revenue = sum(revenue), .groups = "drop")
# Output: one row per store-category combination (20 rows: 4 stores x 5
# categories). .groups = "drop" tells dplyr to return a plain tibble
# afterward, rather than keeping the grouping active for later steps --
# good practice to include every time you group by more than one column.

# --- Chaining group_by + summarise + arrange together ---
sales |>
  group_by(store) |>
  summarise(total_revenue = sum(revenue)) |>
  arrange(desc(total_revenue))
# Output: the same store totals as above, now sorted highest to lowest --
# Utica, Rome, Syracuse, Albany. This three-step chain (group, summarize,
# sort) is probably the single most common pattern you'll write in dplyr.


# ============================================================================
# 5. tidyr -- Reshaping Data Between Long and Wide
# ============================================================================
#
# So far, every result has been "long": one row per group, one column per
# measurement. Sometimes you want "wide" instead -- one row per store, with
# a separate column for each category. tidyr's pivot_wider() and
# pivot_longer() convert between these two layouts.

# First, build a long summary table to reshape:
store_category_totals <- sales |>
  group_by(store, category) |>
  summarise(total_revenue = sum(revenue), .groups = "drop")

store_category_totals
# Output: 20 rows -- one per store-category pair, exactly like the
# group_by(store, category) result above.

# --- pivot_wider(): turn category values into their own columns ---
wide <- store_category_totals |> pivot_wider(names_from = category, values_from = total_revenue)
wide
# Output: 4 rows (one per store), with 5 new columns -- clothing,
# electronics, groceries, "home goods", toys -- each holding that
# store/category's total revenue. names_from says which column's VALUES
# become new column NAMES; values_from says which column's values fill
# those new columns in.

# --- pivot_longer(): reverse it back to the original long shape ---
long_again <- wide |> pivot_longer(cols = -store, names_to = "category", values_to = "total_revenue")
long_again
# Output: back to 20 rows, matching store_category_totals exactly.
# cols = -store means "pivot every column except store"; names_to says
# what to call the new column holding the old column names (here,
# "category"); values_to says what to call the column holding the values.
# pivot_longer() and pivot_wider() are exact inverses of each other --
# confirmed here, since reversing one with the other reproduces the
# original row count precisely.
#
# Connecting this to pandas: pivot_wider() is the equivalent of pandas'
# .pivot() or .pivot_table(), and pivot_longer() is the equivalent of
# pandas' .melt().


# ============================================================================
# 6. Putting It All Together -- A Full Pipeline
# ============================================================================

sales |>
  filter(category == "electronics") |>
  group_by(store) |>
  summarise(total_revenue = sum(revenue), avg_units = mean(units_sold)) |>
  arrange(desc(total_revenue))
# Output:
#   Utica    742057.  44.2
#   Syracuse 735558.  44.8
#   Rome     680236.  43.6
#   Albany   668309.  42.8
#
# Reading this out loud: "start with sales, keep only electronics rows,
# group by store, compute each store's total revenue and average units
# sold, then sort by total revenue highest-first." Four readable steps,
# chained into one pipeline -- filter, group_by, summarise, arrange. This
# is the shape most real dplyr work takes.


# ############################################################################
# GUIDED PRACTICE
# ############################################################################
#
# Work through these yourself before looking at the solutions further down.
# Each one has been tested and confirmed correct.

# --- Exercise 1 -- filter() + summarise() ---
# Find the total revenue for the "groceries" category only.

# YOUR CODE HERE:
# Find the total revenue for the "groceries" category only.
sales |> 
  filter(category == "groceries") |> 
  summarise(total_revenue = sum(revenue))
# Output: A single row showing the combined total revenue across all stores for groceries.


# --- Exercise 2 -- group_by() + summarise() + arrange() ---
# Compute the average units_sold per category, sorted from highest to
# lowest.

# YOUR CODE HERE:
# Compute the average units_sold per category, sorted from highest to
# lowest.
sales |> 
  group_by(category) |> 
  summarise(avg_units = mean(units_sold)) |> 
  arrange(desc(avg_units))
# Output: Categories listed in descending order of their average units sold per transaction.


# --- Exercise 3 -- mutate() with case_when() ---
# Create a new column called "size" that labels each row "Large" if
# units_sold is greater than 60, and "Small" otherwise. Count how many
# rows fall into each label.

# YOUR CODE HERE:
# Create a new column called "size" that labels each row "Large" if
# units_sold is greater than 60, and "Small" otherwise. Count how many
# rows fall into each label.
sales |> 
  mutate(size = case_when(
    units_sold > 60 ~ "Large",
    TRUE ~ "Small"
  )) |> 
  count(size)
# Output: A breakdown showing the exact number of rows labeled "Large" vs. "Small".


# --- Exercise 4 -- group_by() with two columns + pivot_wider() ---
# Compute the average revenue for every store-category combination, then
# reshape it so each category is its own column (one row per store).

# YOUR CODE HERE:
# Compute the average revenue for every store-category combination, then
# reshape it so each category is its own column (one row per store).
sales |> 
  group_by(store, category) |> 
  summarise(avg_revenue = mean(revenue), .groups = "drop") |> 
  pivot_wider(names_from = category, values_from = avg_revenue)
# Output: A wide tibble with 4 rows (one per store) and 5 category columns containing average revenues.


# --- Exercise 5 -- select() with a helper ---
# Using starts_with() or contains(), select only the columns in sales
# whose names contain the letter "e". (Hint: this should match more than
# one column.)

# YOUR CODE HERE:
# Using starts_with() or contains(), select only the columns in sales
# whose names contain the letter "e". (Hint: this should match more than
# one column.)
sales |> select(contains("e"))
# Output: Selects columns like "store", "date", "revenue", etc., that include the letter "e".


# --- Exercise 6 -- %in% ---
# Filter sales down to only rows where category is "toys" or "clothing",
# using %in% rather than two separate == conditions joined with |. Print
# how many rows matched.

# YOUR CODE HERE:
# Filter sales down to only rows where category is "toys" or "clothing",
# using %in% rather than two separate == conditions joined with |. Print
# how many rows matched.
sales |> filter(category %in% c("toys", "clothing"))
# Output: A subset of the dataframe containing only toy and clothing transactions.


# --- Exercise 7 (stretch) -- Full pipeline ---
# Starting from sales: keep only rows where store is "Albany", group by
# category, compute total revenue and number of transactions per
# category, and sort by total revenue descending.

# YOUR CODE HERE:
# Starting from sales: keep only rows where store is "Albany", group by
# category, compute total revenue and number of transactions per
# category, and sort by total revenue descending.
sales |> 
  filter(store == "Albany") |> 
  group_by(category) |> 
  summarise(
    total_revenue = sum(revenue),
    num_transactions = n()
  ) |> 
  arrange(desc(total_revenue))
# Output: Albany's categories summarized by revenue and transaction count, sorted highest first.


# ############################################################################
# SOLUTIONS
# ############################################################################
#
# Try each exercise yourself first. These have been tested and confirmed
# correct.

# --- Solution -- Exercise 1 ---
sales |> filter(category == "groceries") |> summarise(total = sum(revenue))
# Output: 705731.

# --- Solution -- Exercise 2 ---
sales |> group_by(category) |> summarise(avg_units = mean(units_sold)) |> arrange(desc(avg_units))
# Output: groceries 129., clothing 64.3, electronics 43.9, home goods 37.7,
# toys 26.3

# --- Solution -- Exercise 3 ---
sales |> mutate(size = if_else(units_sold > 60, "Large", "Small")) |> count(size)
# Output: Large 1339, Small 2675 (adds up to 4014)
# Note: if_else() is a simpler version of case_when() for exactly two
# outcomes (true/false) -- either one works here, but if_else() is the
# more direct tool when there's only one condition to check.

# --- Solution -- Exercise 4 ---
sales |>
  group_by(store, category) |>
  summarise(avg_rev = mean(revenue), .groups = "drop") |>
  pivot_wider(names_from = category, values_from = avg_rev)
# Output: 4 rows (one per store), 5 category columns of average revenue.

# --- Solution -- Exercise 5 ---
sales |> select(contains("e"))
# Output: date, store, revenue, category all contain the letter "e" --
# only units_sold doesn't, so it's dropped.

# --- Solution -- Exercise 6 ---
sales |> filter(category %in% c("toys", "clothing")) |> nrow()
# Output: 1609 (791 toys + 818 clothing)

# --- Solution -- Exercise 7 ---
sales |>
  filter(store == "Albany") |>
  group_by(category) |>
  summarise(total_revenue = sum(revenue), num_transactions = n()) |>
  arrange(desc(total_revenue))
# Output: electronics highest (668309., 193 transactions), toys lowest
# (76339., 199 transactions)


# ============================================================================
# WRAP-UP
# ============================================================================
#
# Recap: select() with starts_with()/contains(), everything(), renaming,
# and dropping columns; filter() with &, |, %in%, and !is.na(); mutate()
# with multiple new columns at once and case_when()/if_else() for
# conditional logic; group_by() + summarise() with single and multiple
# aggregates, and grouping by more than one column; pivot_wider() and
# pivot_longer() for reshaping between wide and long layouts; and chaining
# all of the above into one full pipeline.
#
# Common mistakes to watch for:
#   - Forgetting .groups = "drop" after group_by() with multiple columns --
#     the grouping can silently stay active and affect a later step
#   - Writing case_when() conditions in the wrong order -- since the FIRST
#     matching condition wins, a broad condition placed too early can
#     "shadow" a more specific one that was meant to catch first
#   - Mixing up names_from/values_from (pivot_wider) or names_to/values_to
#     (pivot_longer) -- it's easy to get these backwards; re-read which
#     column becomes what
#   - Forgetting that mutate() and summarise() are different: mutate()
#     keeps every original row and adds a column; summarise() collapses
#     many rows down into one row per group
#
# Before next class (Nov 16): Class 21 covers R visualization with
# ggplot2 -- the R equivalent of matplotlib/seaborn from Classes 8-9.
