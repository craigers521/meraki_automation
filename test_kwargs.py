def test_kwargs(**kwargs):
    print(kwargs)
    params = {k.strip(): v for k, v in kwargs.items()}
    print(params)
    for k, v in kwargs.items():
        print(k.strip())
        params[f'{k.strip()}[]'] = kwargs[f'{k}']
        params.pop(k.strip())
        print(params)

test_kwargs(key1="someval", tags=["sometag", "someother"], pages="all")
