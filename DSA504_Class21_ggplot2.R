# ============================================================================
# DSA 504 -- Class 21: R Visualization with ggplot2
# Date: Monday, Nov 16
# Reading: R for Data Science 
# ============================================================================
#
# Classes 8 and 9 covered matplotlib and seaborn. Today covers ggplot2 --
# tidyverse's visualization tool, and the most distinctive part of R's data
# ecosystem. The charts will be familiar (scatter, bar, line, histogram,
# box plot); the SYNTAX is a genuinely different way of thinking about
# building a plot, which is worth slowing down for.
#
# Learning goals -- by the end of this file, you will be able to:
#   - Explain ggplot2's "grammar of graphics" -- building a plot by adding
#     layers, instead of calling one function with many arguments
#   - Create scatter plots, bar/column charts, line charts, histograms, and
#     box plots with the appropriate geom_*() function
#   - Map a variable to color or fill, customize titles/labels with labs(),
#     and apply a theme
#   - Use facet_wrap() to create small multiples -- one subplot per group,
#     automatically
#   - Save a plot to a file with ggsave()
#
# HOW TO USE THIS FILE: run it top to bottom in RStudio. Place your cursor
# on any line and press Ctrl+Enter (Windows/Linux) or Cmd+Enter (Mac) to run
# just that line, or highlight a block and run it all at once. Every single
# chart below has actually been rendered and visually confirmed correct,
# not just written to look plausible.
#
# Make sure retail_sales_clean.csv (the same file from Classes 4 onward) is
# in the same folder as this script.

library(tidyverse)

sales <- read_csv("Class19_retail_sales_clean.csv")


# ============================================================================
# 1. The Grammar of Graphics -- How ggplot2 Thinks
# ============================================================================
#
# matplotlib/seaborn build a chart by calling one function with many
# arguments: sns.boxplot(data=sales, x="category", y="revenue", ...).
#
# ggplot2 builds a chart by ADDING layers together with +, starting from a
# base and stacking pieces on top of it:
#   1. ggplot(data, aes(...))  -- the base: which data, which columns map
#      to which part of the chart (aes = "aesthetic mapping")
#   2. + geom_*()              -- a layer: WHAT to draw (points, bars, a
#      line, etc.)
#   3. + labs(), + theme(), etc. -- optional layers: titles, colors, styling
#
# This might feel like more typing for a simple chart, but it means you can
# build up a complex chart piece by piece, and swap one geom_*() for
# another while keeping everything else the same -- which you'll feel the
# benefit of as these examples go on.


# ============================================================================
# 2. Scatter Plots -- geom_point()
# ============================================================================

ggplot(sales, aes(x = units_sold, y = revenue)) +
  geom_point()
# Output: a scatter plot, units_sold on the x-axis, revenue on the y-axis.
# aes(x = ..., y = ...) says WHICH columns go where; geom_point() says
# "draw this as points." Compare to matplotlib:
#   ax.scatter(sales["units_sold"], sales["revenue"])
# Same chart, same two columns -- ggplot2 just names the columns once,
# inside aes(), rather than passing each one as a separate argument.

# --- Mapping a variable to color ---
ggplot(sales, aes(x = units_sold, y = revenue, color = category)) +
  geom_point(alpha = 0.5)
# Output: the same scatter plot, now with points colored by category, and
# a legend added automatically. Each category traces its own distinct
# diagonal line (different categories have different typical prices per
# unit) -- something that's much harder to see without the color mapping.
# alpha = 0.5 makes points semi-transparent, the same idea as Class 8's
# matplotlib alpha argument, useful when points overlap heavily.


# ============================================================================
# 3. Bar and Column Charts -- geom_bar() vs. geom_col()
# ============================================================================
#
# This is a common early mix-up: geom_bar() and geom_col() look similar but
# do different jobs.

# --- geom_bar(): counts rows automatically -- no y needed ---
ggplot(sales, aes(x = store)) +
  geom_bar()
# Output: a bar per store, with height equal to how many ROWS have that
# store -- geom_bar() counts for you. You never gave it a y value, because
# counting IS the point of geom_bar().

# --- geom_col(): plots a value you already computed -- y is required ---
category_totals <- sales |> group_by(category) |> summarise(total_revenue = sum(revenue))
ggplot(category_totals, aes(x = category, y = total_revenue)) +
  geom_col()
# Output: a bar per category, with height equal to total_revenue -- a
# number we already calculated with group_by()+summarise() in Class 20.
# geom_col() expects you to supply the height yourself; it does no
# counting or summarizing on its own. Rule of thumb: if your data is
# already one row per bar with the height you want, use geom_col(). If
# you want ggplot2 to count raw rows for you, use geom_bar().


# ============================================================================
# 4. Line Charts -- geom_line()
# ============================================================================

daily_totals <- sales |> group_by(date) |> summarise(total_revenue = sum(revenue))
ggplot(daily_totals, aes(x = date, y = total_revenue)) +
  geom_line()
# Output: daily total revenue across the whole year -- the direct
# equivalent of Class 8's matplotlib line chart of the same data. Line
# charts need the x-axis to already be in order (here, by date), unlike
# bar/scatter, which don't care about row order.


# ============================================================================
# 5. Histograms -- geom_histogram()
# ============================================================================

ggplot(sales, aes(x = revenue)) +
  geom_histogram(bins = 30)
# Output: the distribution of revenue across all 4,014 transactions.
# bins = 30 controls how many bars the range gets split into -- same idea,
# same gotcha, as matplotlib's bins argument from Class 8: too few bins
# hides real structure, too many makes the shape noisy.


# ============================================================================
# 6. Box Plots -- geom_boxplot()
# ============================================================================

ggplot(sales, aes(x = category, y = revenue)) +
  geom_boxplot()
# Output: one box per category, showing the spread of revenue within each.
# Electronics clearly has the highest median AND the widest spread --
# matching exactly what Class 9's seaborn box plot of this same data
# showed. Same data, same conclusion, a third syntax.


# ============================================================================
# 7. Customizing a Chart -- labs(), theme(), and fill
# ============================================================================

ggplot(category_totals, aes(x = category, y = total_revenue)) +
  geom_col(fill = "steelblue") +
  labs(title = "Total Revenue by Category", x = "Category", y = "Total Revenue ($)") +
  theme_minimal()
# Output: the same bar chart as Section 3, now with a single solid color,
# a real title, cleaner axis labels, and theme_minimal() stripping away
# the default gray background grid. labs() is the direct equivalent of
# matplotlib's ax.set_title()/set_xlabel()/set_ylabel(), just combined
# into one call instead of three.

# --- Mapping fill to a variable, instead of setting one fixed color ---
ggplot(category_totals, aes(x = category, y = total_revenue, fill = category)) +
  geom_col() +
  labs(title = "Total Revenue by Category") +
  theme(legend.position = "none")
# Output: each bar gets its own color automatically, one per category.
# Note the difference from Section 2's color = category: for bars, you
# usually want fill (the inside of the shape), while color controls just
# the outline. theme(legend.position = "none") removes the legend here,
# since the category names are already shown directly under each bar --
# keeping it would just repeat the same information twice.


# ============================================================================
# 8. Faceting -- facet_wrap() for Small Multiples
# ============================================================================
#
# This is a genuinely new idea, not something Classes 8-9 covered directly:
# instead of coloring every group onto ONE chart, facet_wrap() draws a
# separate small subplot for each group automatically, all with matching
# axes so they're easy to compare side by side.

ggplot(sales, aes(x = units_sold, y = revenue)) +
  geom_point(alpha = 0.3) +
  facet_wrap(~ category)
# Output: 5 small scatter plots, one per category, arranged in a grid,
# each labeled with its category name. Compare this to Section 2's single
# color-coded scatter plot -- faceting trades "everything on one crowded
# chart" for "one clean chart per group," which is often easier to read
# once there are more than 2-3 groups to compare.


# ============================================================================
# 9. Saving a Plot -- ggsave()
# ============================================================================

my_chart <- ggplot(category_totals, aes(x = category, y = total_revenue)) +
  geom_col(fill = "darkgreen") +
  labs(title = "Total Revenue by Category")

ggsave("category_revenue_chart.png", my_chart, width = 6, height = 4)
# Saves the chart to a file called category_revenue_chart.png in your
# current folder, 6 inches wide by 4 inches tall. Note the pattern here:
# save the plot into a variable first (my_chart), THEN pass it to
# ggsave() -- this is different from matplotlib's fig.savefig(), which
# saves "whatever was drawn most recently" without needing a named
# variable, but the end result (a saved image file) is the same idea.


# ############################################################################
# GUIDED PRACTICE
# ############################################################################
#
# Work through these yourself before looking at the solutions further down.
# Each one has been tested and confirmed correct.

# --- Exercise 1 -- A basic bar chart with labs() ---
# Compute total revenue per store (group_by + summarise), then create a
# bar chart (geom_col()) with a title and a y-axis label.

# YOUR CODE HERE:
store_totals <- sales |> 
  group_by(store) |> 
  summarise(total_revenue = sum(revenue))


ggplot(store_totals, aes(x = store, y = total_revenue)) +
  geom_col() + geom_col(fill = "yellow") +
  labs(title = "Total Revenue by Store", x = "Store", y = "Total Revenue ($)")


# --- Exercise 2 -- Combining dplyr and ggplot2 in one pipe ---
# Using a single pipe starting from sales, filter down to just the
# "electronics" and "clothing" categories, then pipe the result directly
# into ggplot() to create a box plot of revenue by category. (Hint: a
# dplyr pipe can feed directly into ggplot(), without needing to save an
# intermediate variable first.)

# YOUR CODE HERE:
sales |> 
  filter(category %in% c("electronics", "clothing")) |> 
  ggplot(aes(x = category, y = revenue)) +
  geom_boxplot() +
  labs(title = "Revenue: Electronics vs. Clothing", x = "Category", y = "Revenue ($)")


# --- Exercise 3 -- Monthly line chart ---
# Using mutate() with floor_date(date, "month") (from the lubridate
# package, loaded automatically with tidyverse), group the data into
# months, compute total revenue per month, and create a line chart.

# YOUR CODE HERE:
monthly_totals <- sales |> 
  mutate(month = floor_date(date, "month")) |> 
  group_by(month) |> 
  summarise(total_revenue = sum(revenue))

ggplot(monthly_totals, aes(x = month, y = total_revenue)) +
  geom_line(color = "red", linewidth = 1) +
  labs(title = "Monthly Total Revenue", x = "Month", y = "Total Revenue ($)")


# --- Exercise 4 -- Faceted histogram ---
# Create a histogram of units_sold, faceted by category so each category
# gets its own small histogram.

# YOUR CODE HERE:
ggplot(sales, aes(x = units_sold)) +
  geom_histogram(bins = 30, fill = "brown", color = "white") +
  facet_wrap(~ category) +
  labs(title = "Distribution of Units Sold by Category", x = "Units Sold", y = "Count")


# --- Exercise 5 (stretch) -- Fully customized chart ---
# Create a box plot of revenue by store, with fill mapped to store, a
# real title, no legend (since store names already show on the x-axis),
# and theme_minimal() applied.

# YOUR CODE HERE:
ggplot(sales, aes(x = store, y = revenue, fill = store)) +
  geom_boxplot() +
  labs(title = "Revenue Distribution Across Stores", x = "Store", y = "Revenue ($)") +
  theme_minimal() +
  theme(legend.position = "none")


# ############################################################################
# SOLUTIONS
# ############################################################################
#
# Try each exercise yourself first. These have been tested and confirmed
# correct.

# --- Solution -- Exercise 1 ---
store_totals <- sales |> group_by(store) |> summarise(total_revenue = sum(revenue))

ggplot(store_totals, aes(x = store, y = total_revenue)) +
  geom_col(fill = "darkgreen") +
  labs(title = "Total Revenue by Store", y = "Total Revenue ($)")

# --- Solution -- Exercise 2 ---
sales |>
  filter(category %in% c("electronics", "clothing")) |>
  ggplot(aes(x = category, y = revenue)) +
  geom_boxplot()

# --- Solution -- Exercise 3 ---
monthly <- sales |> mutate(month = floor_date(date, "month")) |> group_by(month) |> summarise(total_revenue = sum(revenue))
ggplot(monthly, aes(x = month, y = total_revenue)) +
  geom_line() +
  geom_point()
# (12 months of data; totals range roughly from $461k to $550k per month)

# --- Solution -- Exercise 4 ---
ggplot(sales, aes(x = units_sold)) +
  geom_histogram(bins = 20) +
  facet_wrap(~ category)

# --- Solution -- Exercise 5 ---
ggplot(sales, aes(x = store, y = revenue, fill = store)) +
  geom_boxplot() +
  labs(title = "Revenue Distribution by Store") +
  theme_minimal() +
  theme(legend.position = "none")


# ============================================================================
# WRAP-UP
# ============================================================================
#
# Recap: the grammar of graphics (ggplot() + aes() + geom_*(), built by
# adding layers with +); geom_point() for scatter plots, including mapping
# a variable to color; geom_bar() (auto-counts) vs. geom_col() (plots a
# value you supply) -- a common early mix-up; geom_line() for trends over
# time; geom_histogram() for distributions; geom_boxplot() for comparing
# spread across groups; labs()/theme()/fill for customization; facet_wrap()
# for small multiples; and ggsave() for saving a chart to a file.
#
# Common mistakes to watch for:
#   - Using geom_bar() when you already have a computed total -- it will
#     try to COUNT your already-summarized rows instead of plotting the
#     value you wanted, producing a chart of height "1" for everything
#   - Using color instead of fill for a bar/column/box chart -- color
#     changes just the outline, which can look like nothing happened
#   - Forgetting that a dplyr pipe (|>) can flow directly into ggplot() --
#     you don't need to save an intermediate variable first (see
#     Exercise 2)
#   - Forgetting the + between ggplot2 layers -- unlike the |> pipe used
#     everywhere else in R this semester, ggplot2 layers are joined with a
#     plain +, which is easy to mix up
#
# Before next class (Nov 18): Class 22 covers reproducible reporting with
# Quarto/R Markdown -- turning an R script like this one into a shareable,
# formatted report. HW6 is assigned that day.
