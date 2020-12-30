#!/usr/bin/env python

"""Convenience wrapper for running the scrapper directly from source tree"""
from src.scrapper import main


if __name__ == '__main__':
    main()

"""
PowerShell Command for counting file recursively per directory. Well suited for datalake management
Get-ChildItem -Directory -Recurse|
	ForEach-Object{
		[pscustomobject]@{
			FullName  = $_.Fullname
			FileCount = $_.GetFiles().Count
		}
	}
"""