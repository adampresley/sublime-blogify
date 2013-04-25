# Class: Blogify
# A Sublime Text plugin to make source code more blog friendly. 
#
# Author:
# 	Adam Presley
#
# Copyright 2013 Adam Presley
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sublime, sublime_plugin
import re
import inspect

class Blogify(sublime_plugin.TextCommand):
	def run(self, edit):
		#
		# Filter definitions
		#
		self._filters = (
			("(?i)&", "&amp;"),
			("(?i)<", "&lt;"),
			("(?i)>", "&gt;"),
			("(?im)^\s+(.*?)", self._filter_leadingSpaces),
		)

		self._settings = sublime.load_settings("Blogify.sublime-settings")

		#
		# Get the contents of the current view
		#
		region = sublime.Region(0, self.view.size())
		text = self.view.substr(region)

		replacedText = self._applyFilters(subject=text)
		print replacedText

	def _applyFilters(self, subject):
		result = subject
		
		for f in self._filters:
			pattern, replacement = f

			#
			# Is the replacement a string or a method call?
			#
			if "im_func" in dir(replacement):
				result = replacement(pattern=pattern, subject=result)
			else:
				result = re.sub(pattern, replacement, result)

		return result

	def _filter_leadingSpaces(self, pattern, subject):
		replacement = ""

		for i in range(self._settings.get("indentNumSpaces")):
			replacement += " "

		return re.sub(pattern, replacement, subject)
