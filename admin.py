from flask import Blueprint, flash, redirect, url_for, jsonify
from cursor import getCursor

# from app import app
admin_page = Blueprint("admin", __name__, static_folder="static", template_folder="templates/admin")