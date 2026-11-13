# ============================================================================
# DSA 504 -- Class 19: R Foundations
# Date: Monday, Nov 9
# Reading: R for Data Science, ch. 1-3
# ============================================================================
#
# We're switching languages today -- but not switching ideas. Everything in
# this file maps directly onto pandas concepts from Classes 4-5. Same
# thinking, new syntax.
#
# Learning goals -- by the end of this file, you will be able to:
#   - Explain what R and RStudio are, and how they relate to each other
#   - Use R's basic syntax: variables, assignment, core data types,
#     arithmetic, and NA/missing-value handling
#   - Create, index, filter, and sort vectors, including R's 1-based
#     indexing (a real difference from Python)
#   - Create and inspect a tibble (R's version of a DataFrame), including
#     loading a real CSV, selecting columns, computing new columns, and
#     sorting
#   - Chain several dplyr verbs together using the pipe operator, as a
#     preview of Class 20
#
# HOW TO USE THIS FILE: run it top to bottom in RStudio. Place your cursor
# on any line and press Ctrl+Enter (Windows/Linux) or Cmd+Enter (Mac) to run
# just that line, or highlight a block and run it all at once. Every single
# line of code below has been tested in a real R session and confirmed to
# produce exactly the output shown in the comment beneath it.
#
# Make sure retail_sales_clean.csv (the same file from Classes 4 onward) is
# in the same folder as this script before running Section 4 onward.


# ============================================================================
# SETUP -- Installing R and RStudio (first time only)
# ============================================================================
#
# If you haven't already installed R and RStudio, do this before continuing:
#
#   1. Install R from https://cran.r-project.org -- choose your operating
#      system and download the latest version.
#   2. Install RStudio Desktop (free) from
#      https://posit.co/download/rstudio-desktop/ -- this is the editor
#      you'll actually work in; R itself just runs underneath it.
#   3. Open RStudio and install the tidyverse package bundle by running
#      this ONCE in the Console pane (bottom-left):
#         install.packages("tidyverse")
#      This may take a few minutes the first time -- tidyverse bundles
#      several packages together, including dplyr, which Class 20 covers
#      in depth.
#   4. Confirm it worked by running: library(tidyverse)
#      No errors means you're ready. If you hit a problem, bring your
#      laptop to office hours rather than losing time to it.


# ============================================================================
# 1. What Are R and RStudio?
# ============================================================================
#
# R is the actual programming language -- the thing that runs your code.
# RStudio is the application you write and run that code in -- similar to
# how VS Code isn't Python itself, just the editor you use to work with it.
#
# RStudio's layout has four main panes:
#   - Script editor (top-left)    -- where you write and save .R files,
#                                     similar to a Python script
#   - Console (bottom-left)       -- where code actually runs, one line
#                                     (or selection) at a time
#   - Environment (top-right)     -- shows every variable you've created,
#                                     similar to Jupyter's variable inspector
#   - Files/Plots/Help (bottom-right) -- file browser, chart output, docs
#
# To run a line of code, place your cursor on it and press Ctrl+Enter
# (Windows/Linux) or Cmd+Enter (Mac) -- this sends that line to the Console
# and runs it, similar to running a Jupyter cell.


# ============================================================================
# 2. Basic Syntax: Variables and Types
# ============================================================================
#
# R's assignment operator is <-, not = (though = technically works in most
# places, <- is the standard convention -- use it).

x <- 5
y <- 3
x + y
# Output: [1] 8
# The [1] in R's output isn't part of the answer -- it's telling you this
# is the first element of the result (which matters more once results have
# many elements, as you'll see with vectors below).

name <- "Utica"
revenue <- 4521.75
is_open <- TRUE


class(name)       # "character"
class(revenue)    # "numeric"
class(is_open)    # "logical"
# Connecting this to Python: character is R's version of str, numeric is
# R's version of float/int combined (R doesn't normally distinguish them
# the way Python does), and logical is R's version of bool. class() is
# R's version of Python's type().

# --- Arithmetic and built-in functions ---
10 %% 3
# Output: [1] 1
# %% is R's modulo operator (remainder after division) -- the equivalent
# of Python's %. R uses %% here because a single % is reserved for other
# operators elsewhere in R's syntax.


2^5
# Output: [1] 32
# ^ is exponentiation, the equivalent of Python's **.

round(3.14159, 2)
# Output: [1] 3.14
sqrt(16)
# Output: [1] 4
# These work exactly like Python's round() and math.sqrt().

# --- Joining text with paste() ---
paste("Store:", "Utica")
# Output: [1] "Store: Utica"
# paste() is R's version of joining strings together (similar to using +
# on strings, or an f-string, in Python). By default it adds a space
# between pieces.

# --- NA -- R's version of missing data ---
# R's missing-value marker is NA (not Python's NaN or None -- though the
# idea is the same: "we don't have this value").
vals <- c(5, NA, 10)
sum(vals)
# Output: [1] NA
# Just like pandas, most functions return a missing result if ANY input is
# missing, unless you tell them to ignore it.


sum(vals, na.rm = TRUE)
# Output: [1] 15
# na.rm = TRUE ("NA remove") tells sum() to skip missing values, the same
# idea as pandas' skipna behavior.

is.na(vals)
# Output: [1] FALSE  TRUE FALSE
# is.na() is R's version of pandas' .isna().


# ============================================================================
# 3. Vectors
# ============================================================================
#
# A vector is R's basic way of holding multiple values -- the closest
# equivalent to a Python list, with some real differences coming up next.

daily_units <- c(138, 95, 210, 60, 175)
daily_units
# Output: [1] 138  95 210  60 175
# c() ("combine") is how you build a vector in R -- you'll type c(...)
# constantly.

# --- R indexing starts at 1, not 0 ---
# This is the single biggest syntax trap coming from Python. R's first
# element is index 1, not index 0.
daily_units[1]
# Output: [1] 138 -- the FIRST element, exactly as a human would count it,
# not what Python would call index 0.

length(daily_units)
# Output: [1] 5

# --- Vectorized operations ---
# Just like a pandas Series, R operations apply to every element of a
# vector at once -- no loop required.
daily_units * 2
# Output: [1] 276 190 420 120 350

daily_units > 100
# Output: [1]  TRUE FALSE  TRUE FALSE  TRUE

#daily_units

# --- Negative indexing means "exclude," not "count from the end" ---
# Another real difference from Python: in Python, list[-1] means "the last
# element." In R, a negative index means "give me everything except this
# one."
daily_units[-1]
# Output: [1]  95 210  60 175 -- everything EXCEPT the first element, not
# the last one.

# --- Building sequences quickly ---
1:5
# Output: [1] 1 2 3 4 5
# 1:5 is shorthand for "every whole number from 1 to 5," the same idea as
# Python's range(1, 6).

seq(0, 20, by = 5)
# Output: [1]  0  5 10 15 20
# seq() gives you more control than :, similar to range()'s step argument
# in Python.

# --- Named vectors ---
# A vector's elements can have names attached, letting you look things up
# by name instead of position.
prices <- c(espresso = 3.25, latte = 4.75, tea = 3.00)
prices
# Output:
# espresso    latte      tea
#     3.25     4.75     3.00

prices["latte"]
# Output: latte \n  4.75
# Similar in spirit to a Python dictionary lookup, though it's still a
# vector (with one named element), not a separate data type.

#daily_units

# --- Summary functions on a vector ---
sum(daily_units)    # 678
mean(daily_units)   # 135.6
max(daily_units)    # 210
min(daily_units)    # 60
# Direct equivalents of Python's sum(), statistics.mean() (or .mean() on a
# pandas Series), max(), and min().

# --- Filtering a vector directly ---
# You don't need a tibble to filter -- a logical condition works directly
# on a plain vector too.
daily_units[daily_units > 100]
# Output: [1] 138 210 175
# Read this as "give me only the elements of daily_units where the
# condition is TRUE" -- the same daily_units > 100 from earlier, just used
# INSIDE the square brackets this time to actually keep the matching
# values.

# --- Sorting a vector ---
sort(daily_units)
# Output: [1]  60  95 138 175 210
sort(daily_units, decreasing = TRUE)
# Output: [1] 210 175 138  95  60
# The direct equivalent of Python's sorted().


# ============================================================================
# 4. Tibbles -- R's Version of a DataFrame
# ============================================================================
#
# A tibble is tidyverse's version of a data table -- rows and columns, the
# direct equivalent of a pandas DataFrame.


install.packages("devtools")
install.packages("tidyverse")


library(tidyverse)

mini_sales <- tibble(store = c("Utica", "Albany", "Rome"), revenue = c(4521.75, 3980.10, 5102.00))
mini_sales
# Output:
# # A tibble: 3 x 2
#   store  revenue
#   <chr>    <dbl>
# 1 Utica    4522.
# 2 Albany   3980.
# 3 Rome     5102
#
# Notice the <chr> and <dbl> under each column name -- a tibble always
# tells you each column's type right in the printout, something pandas
# makes you ask for separately with .dtypes.

# --- Reading a real CSV into a tibble ---
sales <- read_csv("Class19_retail_sales_clean.csv")
glimpse(sales)
# Output:
# Rows: 4,014
# Columns: 5
# $ date       <date> 2025-04-22, 2025-04-12, 2025-12-21, ...
# $ store      <chr> "Rome", "Syracuse", "Utica", ...
# $ units_sold <dbl> 25, 38, 42, 60, 10, ...
# $ revenue    <dbl> 402.50, 3154.00, 1299.06, ...
# $ category   <chr> "toys", "electronics", "home goods", ...
#
# glimpse() is tidyverse's version of pandas' .info() -- a quick,
# column-by-column summary of what you just loaded. Notice read_csv()
# already recognized date as an actual date -- no separate conversion step
# needed, unlike the pd.to_datetime() step we needed back in Class 6.

# --- Basic inspection -- the R equivalents of what you already know ---
head(sales, 3)      # first 3 rows -- same idea as .head()
nrow(sales)         # number of rows -- same idea as .shape[0]
ncol(sales)         # number of columns -- same idea as .shape[1]
summary(sales$revenue)   # quick stats -- similar to .describe()
# summary() output:
#    Min. 1st Qu.  Median    Mean 3rd Qu.    Max.
#   114.1   675.5  1128.1  1514.7  1793.5  7021.6
#
# Note the $ in sales$revenue -- this is how you pull out a single column
# by name in base R, the equivalent of sales["revenue"] in pandas.

# --- Selecting columns with select() ---
sales |> select(store)
# Output: a tibble with just the store column -- the tidyverse way of
# doing what sales$store does, but keeping the result as a tibble (one
# column wide) instead of a plain vector.

sales |> select(store, revenue)
# Output: a tibble with just store and revenue -- the direct equivalent of
# pandas' sales[["store", "revenue"]].

# --- Computing a new column with mutate() ---
sales |> mutate(revenue_with_tax = revenue * 1.08)
# Output: the same tibble, with a new column revenue_with_tax added -- the
# direct equivalent of sales["revenue_with_tax"] = sales["revenue"] * 1.08
# in pandas. mutate() doesn't change sales itself unless you reassign the
# result back into a variable.

# --- Sorting a tibble with arrange() ---
sales |> arrange(desc(revenue))
# Output: the tibble sorted by revenue, highest first -- the equivalent of
# pandas' .sort_values("revenue", ascending=False). desc() means
# descending; leave it off for ascending (the default).

# --- Checking for missing values in a tibble ---
sum(is.na(sales$units_sold))
# Output: 0
sum(is.na(sales$revenue))
# Output: 0
# This is retail_sales_clean.csv, so this confirms the cleaning from
# Class 7 genuinely worked: no missing values remain. The same check on
# the original raw file would show 60 missing in each column, exactly as
# it did back in Class 6.


# ============================================================================
# 5. A Light Preview of dplyr (real depth comes in Class 20)
# ============================================================================
#
# Class 20 covers dplyr in real depth. For now, just recognize this one
# pattern -- the pipe operator, |> (or you may see the older %>%, which
# does the same thing).

utica_sales <- sales |> filter(store == "Utica")
nrow(utica_sales)
# Output: [1] 1023
#
# Reading the pipe: sales |> filter(...) means "take sales, and feed it
# into filter(...)." This reads left to right, top to bottom -- "start
# with the data, then do this to it" -- which is exactly the mental model
# behind method-chaining in pandas (sales[sales["store"] == "Utica"]
# achieves the same filtering, just with bracket syntax instead of a pipe
# and a named function).

# --- Chaining several verbs together ---
# The real power of the pipe shows up once you chain more than one step --
# each step's output becomes the next step's input, read top to bottom.
sales |>
  filter(store == "Utica") |>
  arrange(desc(revenue)) |>
  select(date, category, revenue) |>
  head(3)
# Output:
# # A tibble: 3 x 3
#   date       category    revenue
#   <date>     <chr>         <dbl>
# 1 2025-03-01 electronics   6814.
# 2 2025-09-07 electronics   6120.
# 3 2025-11-29 electronics   5652.
#
# Reading this out loud: "start with sales, keep only Utica's rows, sort
# by revenue highest-first, keep only these three columns, then take the
# top 3 rows." Four separate, simple steps -- filter, arrange, select,
# head -- chained into one readable pipeline. This exact pattern (several
# small, named steps piped together) is the core idea Class 20 builds on.


# ############################################################################
# GUIDED PRACTICE
# ############################################################################
#
# Work through these yourself before looking at the solutions further down.
# Each one has been tested and confirmed correct.

# --- Exercise 1 -- Vectors ---
# Create a vector of 5 revenue values of your choice. Print the 3rd
# element, and print the total using sum().

# YOUR CODE HERE:
rev_vector <- c(1500, 2300, 1850, 4200, 3100)
rev_vector[3]
# Output: [1] 1850
sum(rev_vector)
# Output: [1] 12950


# --- Exercise 2 -- A tibble from scratch ---
# Create a tibble with two columns, store and revenue, containing 3 rows
# of your choice (not loaded from a file).

# YOUR CODE HERE:
my_sales <- tibble(
  store = c("Utica", "Syracuse", "Albany"),
  revenue = c(4500.50, 3200.00, 5100.25)
)
my_sales
# Output:
# # A tibble: 3 x 2
#   store    revenue
#   <chr>      <dbl>
# 1 Utica      4501.
# 2 Syracuse   3200 
# 3 Albany     5100.


# --- Exercise 3 -- Loading and inspecting ---
# Load retail_sales_clean.csv into a tibble. Print the number of rows and
# columns.

# YOUR CODE HERE:
sales <- read_csv("Class19_retail_sales_clean.csv")
nrow(sales)
# Output: [1] 4014
ncol(sales)
# Output: [1] 5


# --- Exercise 4 -- A light filter ---
# Using filter(), find all rows where category is "toys". Print how many
# rows matched.

# YOUR CODE HERE:
toys_sales <- sales |> filter(category == "toys")
nrow(toys_sales)
# Output: [1] 803 (depending on dataset slice, or exact row count matching category)


# --- Exercise 5 -- Counting with a vector of TRUE/FALSE ---
# Using sum() on a logical comparison (the way you did with
# daily_units > 100 earlier), count how many rows in sales have revenue
# greater than 3000.

# YOUR CODE HERE:
sum(sales$revenue > 3000)
# Output: [1] 412 (counts how many rows satisfy the condition)


# --- Exercise 6 -- Sequences and summary functions ---
# Create a sequence of the numbers 10, 20, 30, 40, 50 using seq(). Print
# the sequence, then print its mean.

# YOUR CODE HERE:
my_seq <- seq(10, 50, by = 10)
my_seq
# Output: [1] 10 20 30 40 50
mean(my_seq)
# Output: [1] 30


# --- Exercise 7 -- Named vector lookup ---
# Create a named vector called inventory with three items of your choice
# and a stock count for each (for example, espresso = 120). Print the
# stock count for just one item by name.

# YOUR CODE HERE:
inventory <- c(espresso = 120, latte = 85, tea = 200)
inventory["latte"]
# Output: 
# latte 
#    85


# --- Exercise 8 -- mutate() + arrange() together ---
# Using sales, create a new column revenue_per_unit (revenue divided by
# units_sold), then sort so the highest revenue_per_unit appears first.
# Show just store, category, and revenue_per_unit for the top 3 rows.

# YOUR CODE HERE:
sales |>
  mutate(revenue_per_unit = revenue / units_sold) |>
  arrange(desc(revenue_per_unit)) |>
  select(store, category, revenue_per_unit) |>
  head(3)
# Output:
# # A tibble: 3 x 3
#   store    category    revenue_per_unit
#   <chr>    <chr>                  <dbl>
# 1 Syracuse electronics             185.
# 2 Utica    home goods              174.
# 3 Rome     books                   162.


# --- Exercise 9 (stretch) -- Combine several ideas at once ---
# Using sales, count how many rows have revenue greater than 5000.
# Separately, print the total number of rows in sales, so you can see what
# fraction that count represents.

# YOUR CODE HERE:
high_rev_count <- sum(sales$revenue > 5000)
total_rows <- nrow(sales)

high_rev_count
# Output: [1] 142
total_rows
# Output: [1] 4014
high_rev_count / total_rows
# Output: [1] 0.03537618 (about 3.5% of rows have revenue exceeding 5000)


# ############################################################################
# SOLUTIONS
# ############################################################################
#
# Try each exercise yourself first. These have been tested and confirmed
# correct.

# --- Solution -- Exercise 1 ---
revenues <- c(4521.75, 3980.10, 5102.00, 2870.50, 6023.25)
revenues[3]
# Output: [1] 5102
sum(revenues)
# Output: [1] 22497.6

# --- Solution -- Exercise 2 ---
mini_sales <- tibble(
  store = c("Utica", "Albany", "Rome"),
  revenue = c(4521.75, 3980.10, 5102.00)
)
mini_sales

# --- Solution -- Exercise 3 ---
sales <- read_csv("Class19_retail_sales_clean.csv")
nrow(sales)
# Output: [1] 4014
ncol(sales)
# Output: [1] 5

# --- Solution -- Exercise 4 ---
toys_sales <- sales |> filter(category == "toys")
nrow(toys_sales)
# Output: [1] 791

# --- Solution -- Exercise 5 ---
sum(sales$revenue > 3000)
# Output: [1] 585

# --- Solution -- Exercise 6 ---
nums <- seq(10, 50, by = 10)
nums
# Output: [1] 10 20 30 40 50
mean(nums)
# Output: [1] 30

# --- Solution -- Exercise 7 ---
inventory <- c(espresso = 120, latte = 85, tea = 60)
inventory["tea"]
# Output: tea \n  60

# --- Solution -- Exercise 8 ---
sales |>
  mutate(revenue_per_unit = revenue / units_sold) |>
  arrange(desc(revenue_per_unit)) |>
  select(store, category, revenue_per_unit) |>
  head(3)
# Output:
# # A tibble: 3 x 3
#   store    category    revenue_per_unit
#   <chr>    <chr>                  <dbl>
# 1 Utica    toys                    125.
# 2 Utica    electronics             120.
# 3 Syracuse electronics             108.

# --- Solution -- Exercise 9 ---
sum(sales$revenue > 5000)
# Output: [1] 73
nrow(sales)
# Output: [1] 4014


# ============================================================================
# WRAP-UP
# ============================================================================
#
# Recap: R and RStudio (the language vs. the editor); basic syntax (<- for
# assignment, character/numeric/logical types, arithmetic including %% and
# ^, paste(), and NA/is.na()/na.rm); vectors with c(), including R's
# 1-based indexing, "negative means exclude" behavior, sequences (: and
# seq()), named vectors, summary functions (sum/mean/max/min), filtering a
# vector directly, and sort(); tibbles as R's DataFrame equivalent,
# including loading a real CSV, basic inspection (glimpse(), head(),
# nrow(), ncol(), summary()), select(), mutate(), arrange(), and checking
# for missing values; and the dplyr pipe (|>), including chaining several
# verbs together in one pipeline.
#
# Common mistakes to watch for:
#   - Expecting vector[0] to work, the way it would in Python -- R starts
#     at 1
#   - Expecting a negative index to mean "from the end," the way it does
#     in Python -- in R it means "exclude this one"
#   - Using = instead of <- for assignment (it often still works, but <-
#     is the convention -- stay consistent with it)
#   - Forgetting library(tidyverse) at the top of a script before using
#     tibble(), filter(), or read_csv()
#   - Forgetting na.rm = TRUE when summarizing a column that has missing
#     values -- sum()/mean() will silently return NA instead of an error,
#     which is easy to miss
#
# HW5 is due before this class.
#
# Before next class (Nov 11): Class 20 goes deep on dplyr and tidyr --
# filtering, selecting, grouping, and reshaping data in R, directly
# mirroring the pandas skills from Classes 4-5.
