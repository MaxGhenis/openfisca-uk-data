from openfisca_uk_data.datasets.frs.raw_frs import RawFRS
from pathlib import Path
from typing import List
from openfisca_core.model_api import *
from openfisca_uk_data.utils import *
import pandas as pd
import shutil
from openfisca_uk_data.utils import (
    CAPITAL_INCOME_VARIABLES,
    LABOUR_INCOME_VARIABLES,
    uprated,
)
import h5py
from openfisca_uk_data.datasets.frs.base_frs.dataset import BaseFRS
from openfisca_uk_data.datasets.frs.base_frs.model_input_variables import (
    get_input_variables,
)


def from_FRS(year: int = 2018):
    from openfisca_uk import CountryTaxBenefitSystem

    system = CountryTaxBenefitSystem()
    variables = []
    for variable in get_input_variables():
        try:
            variables += [type(system.variables[variable.__name__])]
        except:
            variables += [variable]
    for i in range(len(variables)):
        variable = variables[i]
        if variable.__name__ in LABOUR_INCOME_VARIABLES:
            variables[i] = uprated(
                "uprating.labour_income", from_year=year + 1
            )(variable)
        elif variable.__name__ in CAPITAL_INCOME_VARIABLES:
            variables[i] = uprated(
                "uprating.labour_income", from_year=year + 1
            )(variable)
        else:
            variables[i] = uprated(from_year=year + 1)(variable)

    class reform(Reform):
        def apply(self):
            for var in variables:
                self.update_variable(var)

    return reform


@dataset
class FRS:
    name = "frs"
    model = UK
    input_reform_from_year = from_FRS

    def generate(year) -> None:
        base_frs_years = BaseFRS().years
        if len(base_frs_years) == 0:
            raw_frs_years = RawFRS().years
            if len(raw_frs_years) == 0:
                raise Exception("No FRS microdata to generate from")
            else:
                base_frs_year = max(raw_frs_years)
        else:
            base_frs_year = max(base_frs_years)
        from openfisca_uk import Microsimulation

        base_frs_sim = Microsimulation(dataset=BaseFRS, year=base_frs_year)
        person_vars, benunit_vars, household_vars = [
            [
                var.__name__
                for var in get_input_variables()
                if var.entity.key == entity
            ]
            for entity in ("person", "benunit", "household")
        ]
        with h5py.File(FRS.file(year), mode="w") as f:
            for variable in person_vars + benunit_vars + household_vars:
                try:
                    f[f"{variable}/{year}"] = base_frs_sim.calc(
                        variable, year
                    ).values
                except:
                    f[f"{variable}/{year}"] = base_frs_sim.calc(
                        variable, year
                    ).values.astype("S")
