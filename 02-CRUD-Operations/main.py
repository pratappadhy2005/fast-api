from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional

app = FastAPI()


class Patient(BaseModel):
    id: Annotated[str, Field(..., description='ID of the patient in the DB',
                             example='P001', min_length=3, max_length=5)]
    name: Annotated[str, Field(..., description='Name of the patient',
                               example='John Doe', min_length=3, max_length=50)]
    city: Annotated[str, Field(..., description='City of the patient',
                               example='New York', min_length=3, max_length=50)]
    age: Annotated[int, Field(..., description='Age of the patient',
                              example=30, gt=0, lt=120)]
    gender: Annotated[Literal['male', 'female', 'other'], Field(..., description='Gender of the patient',
                                                                example='male')]
    height: Annotated[float, Field(..., description='Height of the patient in meters',
                                   example=1.75, gt=0, lt=3)]
    weight: Annotated[float, Field(..., description='Weight of the patient in kgs',
                                   example=75, gt=0, lt=300)]

    @computed_field
    @property
    def calculate_bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.calculate_bmi < 18.5:
            return 'Underweight'
        elif self.calculate_bmi < 25:
            return 'Normal'
        elif self.calculate_bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'


class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)

    return data


def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f, indent=2)


@app.get("/")
def hello():
    return {'message': 'Patient Management System API'}


@app.get('/about')
def about():
    return {'message': 'A fully functional API to manage your patient records'}


@app.get('/view')
def view():
    data = load_data()

    return data


@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description='ID of the patient in the DB', example='P001')):
    # load all the patients
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient not found')


@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='Sort on the basis of height, weight or bmi', example='height'), order: str = Query('asc', description='Sort in ascending or descending order', example='asc')):
    valid_fields = ['height', 'weight', 'bmi']
    valid_orders = ['asc', 'desc']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail='Invalid field to sort by')

    if order not in valid_orders:
        raise HTTPException(status_code=400, detail='Invalid order to sort by')

    data = load_data()

    sort_order = True if order == 'desc' else False

    sorted_data = sorted(
        data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data


@app.post('/create')
def create_patient(patient: Patient):
    data = load_data()

    # check if patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')

    # add the patient
    data[patient.id] = patient.model_dump(exclude=['id'])

    # save the data
    save_data(data)

    return JSONResponse(status_code=201, content={'message': 'Patient created successfully'})


@app.put('/update/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')

    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    # existing_patient_info -> pydantic object -> updated bmi + verdict
    existing_patient_info['id'] = patient_id
    patient_pydantic_object = Patient(**existing_patient_info)

    # pydantic object -> dict
    existing_patient_info = patient_pydantic_object.model_dump(exclude='id')

    data[patient_id] = existing_patient_info

    save_data(data)
    return JSONResponse(status_code=200, content={'message': 'Patient updated successfully'})


@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=200, content={'message': 'Patient deleted successfully'})
