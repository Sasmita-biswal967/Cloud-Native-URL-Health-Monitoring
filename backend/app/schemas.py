from pydantic import BaseModel


class URLRequest(BaseModel):
    url: str


class URLResponse(URLRequest):
    id: int
    status: str
    status_code: int
    response_time: float

    class Config:
        from_attributes = True