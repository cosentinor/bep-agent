from marshmallow import Schema, fields, validate


non_empty_str = validate.Length(min=1)


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=non_empty_str)


class RegisterSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=2))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))
    role = fields.String(load_default='viewer', validate=validate.OneOf(['admin', 'contributor', 'viewer']))


class ProjectCreateSchema(Schema):
    name = fields.String(required=True, validate=non_empty_str)
    location = fields.String(required=True, validate=non_empty_str)
    client = fields.String(required=True, validate=non_empty_str)
    delivery_method = fields.String(load_default='Design-Bid-Build')
    description = fields.String(load_default='')


class GoalCreateSchema(Schema):
    project_id = fields.Integer(required=True)
    description = fields.String(required=True, validate=non_empty_str)
    bim_use = fields.String(required=True, validate=non_empty_str)
    success_metric = fields.String(load_default='')
    priority = fields.String(load_default='medium', validate=validate.OneOf(['low', 'medium', 'high']))
    status = fields.String(load_default='pending', validate=validate.OneOf(['pending', 'in-progress', 'completed']))


class TIDPCreateSchema(Schema):
    project_id = fields.Integer(required=True)
    description = fields.String(required=True, validate=non_empty_str)
    responsible_user_id = fields.Integer(load_default=None, allow_none=True)
    due_date = fields.Date(required=True, format='%Y-%m-%d')
    file_format = fields.String(load_default='IFC')
    status = fields.String(load_default='pending', validate=validate.OneOf(['pending', 'in-progress', 'completed', 'overdue']))
    notes = fields.String(load_default='')


