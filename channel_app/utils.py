def row2dict(row, column_list=None):
    d = {}
    if column_list == None:
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))
    else:
        for column in column_list:
            d[column] = str(getattr(row, column))
    return d