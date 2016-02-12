#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

# `i` is a LINK, not a copy

a= [[1,2],[2,3],[5,6]]

for n, i in enumerate(a):
	print(id(i))
	print(id(a[n]))

	for j in range(2):
		print(i)
		a[n][0] = 10
