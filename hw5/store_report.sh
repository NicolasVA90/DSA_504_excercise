#!/bin/bash
# Loop through stores, calculate revenue, and add [HIGH PERFORMER] label if > 5000

rm -f store_report.txt
for store in Utica Albany Rome Syracuse; do
    awk -F',' -v s="$store" '
    $2 == s {sum += $4} 
    END {
        if (sum > 5000)
            print s ": " sum " [HIGH PERFORMER]";
        else
            print s ": " sum;
    }' sales_log.txt >> store_report.txt
done
