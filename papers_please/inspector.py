from itertools import combinations
from collections import defaultdict
from datetime import date
from re import compile

from .generator_utils import documents, countries, get_comma_split

states = set(map(str.lower, countries))
glory_nation = countries[0].lower()
mismatching = {
    'NAME': 'name',
    'NATION': 'nationality',
    'ID#': 'ID number',
    'DOB': 'date of birth'
}

find_papers = compile(r'([^:]+): (.+)\n?')
find_constraints = compile(
    r'wanted by the state: (?P<wanted>.+)|'
    r'(?P<action>allow) citizens of (?P<who>(?:[\w ]+|, )+)|'
    r'(?:citizens of )?(?P<who2>.+?) require (?P<piece>[\w ]+)'
)


class Inspector(object):
    """Check a bulletin and make a access control decision."""
    def __init__(self):
        self.allowed = {c: False for c in states}
        self.docs, self.vacs = defaultdict(set), defaultdict(set)
        self.wanted, self.papers, self.papers_set = None, None, None

    def receive_bulletin(self, bulletin):
        """Keep most important bulletin data in properties."""

        # Arstotzka is always allowed country cause it's your country.
        self.allowed[glory_nation] = True

        # Match bulletin data.
        for m in find_constraints.finditer(bulletin.lower()):

            # Add criminal entrant to cache.
            if m['wanted']:
                self.wanted = get_comma_split(m['wanted'])
                continue

            who = (m['who'] or m['who2']).split(', ')
            if who == ['entrants']:
                who = states
            elif who == ['foreigners']:
                who = states - {glory_nation}

            # Add allowed countries to cache.
            if m['action']:
                for country in who:
                    self.allowed[country] = m['action'] == 'allow'
            else:
                # Add required documents to cache.
                piece = m['piece'].replace(' ', '_')
                doctype = self.docs

                # Add required vaccination to cache.
                if piece.endswith('vaccination'):
                    piece = piece.replace('_vaccination', '')
                    doctype = self.vacs

                for w in who:
                    doctype[w].add(piece)

    def __get_mismatched_papers(self):
        """Search for mismatching in papers data."""
        for p1, p2 in combinations(self.papers, 2):
            p1, p2 = self.papers[p1], self.papers[p2]
            for k in set(p1) & set(p2) - {'EXP'}:
                if k in mismatching and p1[k] != p2[k]:
                    return mismatching[k]

    def __get_missing_docs(self, nation):
        """Search for missing documents."""
        required = set(self.docs.get(nation, {documents[0]}))
        if self.vacs[nation]:
            required.add(documents[1])

        return required - self.papers_set

    def __is_wanted(self):
        """Match in case of entrant is a wanted criminal."""
        return any(
            get_comma_split(contents.get('NAME', 0)) == self.wanted
            for _, contents in self.papers.items()
        )

    def __is_banned(self, nation):
        """Match in case of entrant from banned country."""
        return not self.allowed.get(nation, 0)

    def inspect(self, papers):
        """Check entrant papers and make access decision."""
        # Split document content to dictionary values.
        self.papers = {
            docs: {
                k: v.lower() for k, v in find_papers.findall(contents)
            }
            for docs, contents in papers.items()
        }
        self.papers_set = set(self.papers)
        mismatched = self.__get_mismatched_papers()

        # Match in case of entrant hasn't required document.
        nation = next((
            contents['NATION'] for _, contents in self.papers.items()
            if 'NATION' in contents
        ), '')
        missing_docs = self.__get_missing_docs(nation)

        # Match in case of one of entrant documents is expired.
        # Edge date is today.
        expired_docs = next(
            (docs.replace('_', ' ') for docs, contents in self.papers.items()
             if 'EXP' in contents and date(
                *map(int, contents['EXP'].split('.'))
            ) <= date.today()), None)
        # Match in case of entrant hasn't required vaccination.
        vaccines = set(
            self.papers.get(
                documents[1], {}).get('VACCINES', '').replace(
                ' ', '_').split(',_')
        )
        mis_vaccines = self.vacs[nation] - vaccines

        is_foreign = nation != glory_nation
        is_bad_diploma = False
        # Delete access permit requirement
        # if a foreigner has another access document.
        if is_foreign and documents[2] in missing_docs:
            substitute = set(documents[2:]) & self.papers_set
            if substitute:
                missing_docs.discard(documents[2])
            # Turn value into "True" if Arstotzka is in access line.
            is_bad_diploma = (
                    substitute == {documents[4]} and glory_nation
                    not in self.papers[documents[4]]['ACCESS']
            )

        # The judgment order of decision operations with invalid documents
        answer = False
        if self.__is_wanted():
            return answer, 'Detainment: Entrant is a wanted criminal.'
        if mismatched:
            return answer, f'Detainment: {mismatched} mismatch.'
        if missing_docs:
            return answer, f'Entry denied: missing ' \
                f'required {missing_docs.pop().replace("_", " ")}.'
        if is_bad_diploma:
            return answer, 'Entry denied: invalid diplomatic authorization.'
        if self.__is_banned(nation):
            return answer, 'Entry denied: citizen of banned nation.'
        if expired_docs:
            return answer, f'Entry denied: {expired_docs} expired.'
        if mis_vaccines:
            return answer, 'Entry denied: missing required vaccination.'

        # Reach in case of documents are valid.
        answer = True
        return (answer, 'Cause no trouble.') if is_foreign \
            else (answer, 'Glory to Arstotzka.')

    def clear(self):
        """
        Delete all saved properties data.
        If this method is not used, there will be a conflict with next bulletin.
        """
        self.allowed = {c: False for c in states}
        self.docs, self.vacs = defaultdict(set), defaultdict(set)
        self.wanted, self.papers, self.papers_set = None, None, None
