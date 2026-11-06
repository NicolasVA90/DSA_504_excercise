#!/bin/bash
# Description: Look up sales records by category argument ($1) and count matching rows

echo "Matching rows for category: $1"
grep "$1" sales_log.txt

echo "Total matching rows:"
grep -c "$1" sales_log.txt
