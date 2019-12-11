from random import choice, choices, randrange

from .generator_utils import (
    documents, countries, purposes,
    get_comma_sep, make_choice, make_shuffle,
    add_countries, add_id_number, add_vaccinations, add_name_and_sex, add_date
)


class DataStarterPack(object):
    """Create game data for every single day."""

    def __init__(self, bandwidth):
        self.bandwidth = bandwidth
        self.states = add_countries(5)
        self.vacs = add_vaccinations(2)

        self.id_data = [add_id_number() for _ in range(bandwidth)]
        self.all_states = [
            choice([countries[0]] + self.states) for _ in range(self.bandwidth)
        ]
        self.birth_dates = [add_date('-49y', '-18y') for _ in range(bandwidth)]
        self.passport_exp_dates = [
            add_date('now', '+5y') for _ in range(bandwidth)
        ]
        self.access_exp_dates = [
            add_date('now', '+2y') for _ in range(bandwidth)
        ]

        names_and_genders = [add_name_and_sex() for _ in range(bandwidth)]
        self.names = [name for name, _ in names_and_genders]
        self.genders = [sex for _, sex in names_and_genders]

    @make_choice
    def __states_reqs(self):
        return self.states, 2

    def __choose_reqs(self, reqs):
        """Select categories of entrants that require documents."""
        who = 'Entrants'

        if reqs != documents[0]:
            num = 0 if reqs.startswith('access') else randrange(3)
            if not num:
                who = 'Foreigners'
            elif num == 1:
                # Select one or two countries from the list of allowed.
                new_states = get_comma_sep(self.__states_reqs())
                who = f'Citizens of {new_states}'
        return f'{who} require {reqs}'

    def create_bulletin(self):
        """Create bulletin data for every single day."""
        bulletin = []

        # Passport is required for all entrants permanently.
        # Access permit is required for all foreigners permanently.
        # One of the vaccinations may be required for all citizens,
        # as well as only for foreigners or for individual countries.
        bulletin.extend([self.__choose_reqs(documents[0]),
                         f'Allow citizens of {get_comma_sep(self.states)}',
                         self.__choose_reqs(documents[2].replace('_',' ')),
                         self.__choose_reqs(f'{choice(self.vacs)} '
                                            f'vaccination')])

        # Add criminal entrant (50% probability).
        if randrange(2):
            wanted = choice(self.names)
            bulletin.append(f'Wanted by the state: {wanted}')

        return '\n'.join(bulletin)

    def __create_fraud_data(
            self, id_data, names, dob, pass_exp, acc_exp, states, vacs):
        """
        Randomly select papers data to change it.
        The goal is to create fake documents for gaming process.
        """

        fails = (self.bandwidth + 1) // 2  # change at least 50% of documents

        while fails:
            num = randrange(8)

            # Add new data to entrant documents.
            if not num:
                id_data[fails - 1] = add_id_number()
            elif num == 1:
                names[fails - 1], _ = add_name_and_sex()
            elif num == 2:
                dob[fails - 1] = add_date('-49y', '-10y')
            elif num == 3:
                pass_exp[fails - 1] = add_date('-1M', 'now')
            elif num == 4:
                acc_exp[fails - 1] = add_date('-1M', 'now')
            elif num == 5:
                states[fails - 1] = choice(self.states)

            elif num == 6:
                # Add countries from banned list.
                states[fails - 1] = choice(
                    list(set(countries) - set(self.states))
                )
                self.all_states[fails - 1] = states[fails - 1]

            else:
                # Select one of three operations:
                # - delete vaccination from top of the list
                # - delete vaccination from end of the list
                # - add completely new vaccinations
                vac_num = randrange(3)
                if not vac_num:
                    del vacs[fails - 1][0]
                elif vac_num == 1:
                    del vacs[fails - 1][-1]
                else:
                    vacs[fails - 1] = add_vaccinations(3)

            fails -= 1

        return id_data, names, dob, pass_exp, acc_exp, states, vacs

    def __missing_doc(self, entrants):
        """
        Randomly select document to delete it.
        The goal is to create missing of documents for gaming process.
        Probability is 50%.
        """
        if randrange(2):
            num = randrange(self.bandwidth)
            missing_first = choice(documents[:3])

            # Reach in case of a foreigner has another access document.
            # Probability is 16,6%.
            if not randrange(3):
                missing_second = choice(documents[3:])
                if missing_second in entrants[num]:
                    del entrants[num][missing_second]

            if missing_first in entrants[num]:
                del entrants[num][missing_first]

        return entrants

    def create_papers(self):
        """
        Create entrant papers for every single day. The range of entrants
        depends on user-defined bandwidth.
        """

        entrants = []

        all_vacs = [list(set(self.vacs + add_vaccinations(1)))
                    for _ in range(self.bandwidth)]

        # Assign mismatching and fake documents.
        fraud_id_data, fraud_names, fraud_birth_dates, \
            fraud_passport_dates, fraud_access_dates, \
            fraud_countries, fraud_vacs = self.__create_fraud_data(
                self.id_data[:], self.names[:], self.birth_dates[:],
                self.passport_exp_dates[:], self.access_exp_dates[:],
                self.all_states[:], all_vacs
            )

        for i in range(self.bandwidth):
            # Mix valid and fake documents.
            shuffled_name = make_shuffle([self.names[i], fraud_names[i]], 2)
            shuffled_dob = make_shuffle(
                [self.birth_dates[i], fraud_birth_dates[i]], 2
            )
            shuffled_vacs = make_shuffle(fraud_vacs[i], len(fraud_vacs[i]))

            # Add random access countries to diplomatic authorization
            # and add Arstotzka in a probability of 66,6%.
            access_countries = add_countries(2)
            if randrange(3):
                access_countries += [countries[0]]
            shuffled_countries = make_shuffle(
                access_countries, len(access_countries)
            )

            # Delete your country from diplomatic authorization.
            if fraud_countries[i] in shuffled_countries:
                del shuffled_countries[
                    shuffled_countries.index(fraud_countries[i])
                ]
            if self.all_states[i] in shuffled_countries:
                del shuffled_countries[
                    shuffled_countries.index(self.all_states[i])
                ]

            # Add previously defined content to papers.
            passport_data = f'ID#: {fraud_id_data[i]}\n' \
                            f'NATION: {fraud_countries[i]}\n' \
                            f'NAME: {self.names[i]}\n' \
                            f'DOB: {self.birth_dates[i]}\n' \
                            f'SEX: {self.genders[i]}\n' \
                            f'EXP: {fraud_passport_dates[i]}'
            vac_data = f'NAME: {shuffled_name[0]}\n' \
                       f'DOB: {shuffled_dob[0]}\n' \
                       f'VACCINES: {get_comma_sep(shuffled_vacs)}'

            common_data = f'NAME: {shuffled_name[1]}\n' \
                          f'NATION: {self.all_states[i]}\n' \
                          f'ID#: {self.id_data[i]}\n'
            access_data = f'PURPOSE: {choice(purposes)}\n' \
                          f'EXP: {fraud_access_dates[i]}'
            asylum_data = f'DOB: {shuffled_dob[1]}\n' \
                          f'EXP: {fraud_access_dates[i]}'
            diploma_data = f'ACCESS: {get_comma_sep(shuffled_countries)}'

            # Select foreigner access document:
            # - 50% probability of access permit
            # - 25% probability of grant of asylum
            # - 25% probability of diplomatic authorization
            data_choice = choice([access_data, access_data,
                                  asylum_data, diploma_data])
            foreigner_data = common_data + data_choice

            doc_dict = {
                access_data: documents[2],
                asylum_data: documents[3],
                diploma_data: documents[4]
            }
            entrant = {
                documents[0]: passport_data,
                documents[1]: vac_data,
            }
            # Access permit isn't required if nation is Arstotzka.
            if fraud_countries[i] != countries[0]:
                entrant = {
                    documents[0]: passport_data,
                    documents[1]: vac_data,
                    doc_dict.get(data_choice): foreigner_data
                }
            entrants.append(entrant)

        return make_shuffle(self.__missing_doc(entrants), self.bandwidth)
