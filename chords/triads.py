class GeneratorError(Exception): pass

class ProgressionGenerator:
	# diatonic triads for major keys
	diatonic_triads = [
		('C', 'Dm', 'Em', 'F', 'G', 'Am', 'Bdim'),
		('G', 'Am', 'Bm', 'C', 'D', 'Em', 'F#dim'),
		('D', 'Em', 'F#m', 'G', 'A', 'Bm', 'C#dim'),
		('A', 'Bm', 'C#m', 'D', 'E', 'F#m', 'G#dim'),
		('E', 'F#m', 'G#m', 'A', 'B', 'C#m', 'D#dim'),
		('B', 'C#m', 'D#m', 'E', 'F#', 'G#m', 'A#dim'),
		('F#', 'G#m', 'A#m', 'B', 'C#', 'D#m', 'E#dim'),
		('Db', 'Ebm', 'Fm', 'Gb', 'Ab', 'Bbm', 'Cdim'),
		('Ab', 'Bbm', 'Cm', 'Db', 'Eb', 'Fm', 'Gdim'),
		('Eb', 'Fm', 'Gm', 'Ab', 'Bb', 'Cm', 'Ddim'),
		('Bb', 'Cm', 'Dm', 'Eb', 'F', 'Gm', 'Adim'),
		('F', 'Gm', 'Am', 'Bb', 'C', 'Dm', 'Edim'),
		]

	numerals_table = {
		'I': '1',
		'ii': '2',
		'iii': '3',
		'IV': '4',
		'V': '5',
		'vi': '6',
		'VII': '7',
	}

	def _is_allowed_numeral(self, numeral):
		return numeral in self.numerals_table or numeral in self.numerals_table.values()

	def _to_indexes(self, numerals):
		"""numerals -- valid numerals
		returns indexes (list) -- usable indexes for ProgressionGenerator.diatonic_triads
		"""
		indexes = []
		for numeral in numerals:
			if numeral in self.numerals_table:
				n = int(self.numerals_table[numeral])
			else:
				n = int(numeral)
			indexes.append(n-1) # indexes are zero based
		return indexes

	def _get_chords(self, chords, indexes):
		"""chords (list) -- chords to choose from
		indexes (list) -- which chords to choose
		returns (list)
		"""
		return [chords[i] for i in indexes]

	def _to_numerals(self, prog):
		"""prog (string) -- line of numerals
		returns numerals (list)
		throws GeneratorError on incorrect format
		"""
		if '-' in prog:
			numerals = prog.split('-')
		elif ' ' in prog:
			numerals = prog.split(' ')
		elif len(prog) == 1:
			numerals = [prog]
		else:
			raise GeneratorError('Incorrect format.')
		return numerals

	def _parse_input(self, prog):
		"""prog (string) -- line of numerals
		returns numerals (list) -- valid numerals
		throws GeneratorError on incorrect input
		"""
		prog = prog.strip()
		numerals = self._to_numerals(prog)
		for numeral in numerals:
			if not self._is_allowed_numeral(numeral):
				raise GeneratorError('{} isn\'t allowed numeral.'.format(numeral))
		return numerals


	def get_progressions(self, prog):
		"""Acceptable inputs:
		1)'I V vi IV' (separated by a single space)
		2)'V-vi-I-I-vi' (separated by hyphen)
		3)'1 5 6 4' (as numbers)
		4)'6 4' (variable length)
		etc
		Unacceptable inputs:
		1)'i V' (1 can't be minor)
		2)'1 8' (7 is maximum)
		3)'3.50' (No Loch Ness monsters allowed)

		Return value format (example):
		[
			{'input_numerals': ['I', 'V', 'vi', 'IV']},
			{'key': 'C', 'chords': ['C', 'G', 'Am', 'F']},
			{'key': 'G', 'chords': ['G', 'D', 'Em', 'C']},
			...
		]

		prog (string) -- see above
		returns progressions (list) -- see above
		"""
		numerals = self._parse_input(prog)
		indexes = self._to_indexes(numerals)
		progressions = [{
			'input_numerals': numerals,
		}]
		for chords in self.diatonic_triads:
			progressions.append({
				'key': chords[0], 
				'chords': self._get_chords(chords, indexes),
				})

		return progressions