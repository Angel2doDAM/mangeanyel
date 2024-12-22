# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime


class task(models.Model):
    _name = "manageanyel.task"
    _description = "manageanyel.task"

    code = fields.Char(string="Código", compute="_get_code")
    name = fields.Char(
        string="Nombre", readonly=False, required=True, help="Introduzca el nombre"
    )
    description = fields.Text(string="Descripción")
    start_date = fields.Datetime(string="fecha Inicio")
    end_date = fields.Datetime(string="fecha Fin")
    is_paused = fields.Boolean(string="Pausado")

    sprint_id = fields.Many2one(
        "manageanyel.sprint",
        string="Sprint",
        # required=True,
        ondelete="cascade",
        compute="_get_sprint",
        store=True,
    )

    history_id = fields.Many2one(
        "manageanyel.history", string="Historias", required=True, ondelete="cascade"
    )

    technologys_id = fields.Many2many(
        comodel_name="manageanyel.technology",
        relation="technology_task",
        colum1="technologys_ids",
        colum2="tasks_ids",
    )

    def _get_code(self):
        for task in self:
            task.code = "TASK_" + str(task.id)

    @api.depends("code")
    def _get_sprint(self):
        for task in self:
            sprints = self.env["manageanyel.sprint"].search(
                [("project_id.id", "=", task.history_id.project_id.id)]
            )
            found = False
            for sprint in sprints:
                if (
                    isinstance(sprint.end_date, datetime.datetime)
                    and sprint.end_date > datetime.datetime.now()
                ):
                    task.sprint_id = sprint.id
                    found = True
            if not found:
                task.sprint_id = False


class sprint(models.Model):
    _name = "manageanyel.sprint"
    _description = "manageanyel.sprint"

    name = fields.Char(
        string="Nombre", readonly=False, required=True, help="Introduzca el nombre"
    )
    description = fields.Text(string="Descripción")
    start_date = fields.Datetime(string="Fecha Inicio")
    duration = fields.Integer(string="Duración")
    end_date = fields.Datetime(string="fecha Fin", compute="_get_end_date", store=True)

    project_id = fields.Many2one(
        "manageanyel.project", string="Proyectos", required=True, ondelete="cascade"
    )

    tasks_id = fields.One2many(
        string="Tasks", comodel_name="manageanyel.task", inverse_name="sprint_id"
    )

    @api.depends("start_date", "duration")
    def _get_end_date(self):
        for sprint in self:
            if isinstance(sprint.start_date, datetime.datetime) and sprint.duration > 0:
                sprint.end_date = sprint.start_date + datetime.timedelta(
                    days=sprint.duration
                )
            else:
                sprint.end_date = sprint.start_date


class project(models.Model):
    _name = "manageanyel.project"
    _description = "manageanyel.project"

    name = fields.Char(
        string="Nombre", readonly=False, required=True, help="Introduzca el nombre"
    )
    description = fields.Text(string="Descripción")

    sprints_id = fields.One2many(
        string="Sprints", comodel_name="manageanyel.sprint", inverse_name="project_id"
    )

    historys_id = fields.One2many(
        string="Historias",
        comodel_name="manageanyel.history",
        inverse_name="project_id",X
    )


class history(models.Model):
    _name = "manageanyel.history"
    _description = "manageanyel.history"

    name = fields.Char(
        string="Nombre", readonly=False, required=True, help="Introduzca el nombre"
    )
    description = fields.Text(string="Descripción")
    
    project_id = fields.Many2one(
        "manageanyel.project", string="Proyectos", required=True, ondelete="cascade"
    )

    tasks_id = fields.One2many(
        string="Tareas", comodel_name="manageanyel.task", inverse_name="history_id"
    )

    used_technologies = fields.Many2many(
        "manageanyel.technology", compute="_get_used_technologies"
    )

    def _get_used_technologies(self):
        for history in self:
            technologies = None
            for task in history.tasks_id:
                if not technologies:
                    technologies = task.technologys_id
                else:
                    technologies = technologies + task.technologys_id
        history.used_technologies = technologies


class technology(models.Model):
    _name = "manageanyel.technology"
    _description = "manageanyel.technology"

    name = fields.Char(
        string="Nombre", readonly=False, required=True, help="Introduzca el nombre"
    )
    description = fields.Text(string="Descripción")
    photo = fields.Image(string="Imagen")

    tasks_id = fields.Many2many(
        comodel_name="manageanyel.task",
        relation="technology_task",
        colum1="technologys_ids",
        colum2="tasks_ids",
    )

    history_id2 = fields.Many2many(
        comodel_name="manageanyel.history",
        relation="technology_task",
        colum1="technologys_ids",
        colum2="history_ids",
    )
