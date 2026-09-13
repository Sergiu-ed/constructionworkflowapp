import os
from datetime import datetime

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///app.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256), nullable=True)


class WorkRequest(db.Model):
    __tablename__ = "work_requests"

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(180), nullable=True)
    phone = db.Column(db.String(64), nullable=True)
    category = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    postal_code = db.Column(db.String(20), nullable=True)
    budget_sek = db.Column(db.Float, nullable=True)
    urgency = db.Column(db.String(30), nullable=False, default="flexible")
    status = db.Column(db.String(30), nullable=False, default="new")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Contractor(db.Model):
    __tablename__ = "contractors"

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(160), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    categories = db.Column(db.String(500), nullable=False, default="")
    hourly_rate_sek = db.Column(db.Float, nullable=True)
    rating = db.Column(db.Float, nullable=False, default=0)
    completed_jobs = db.Column(db.Integer, nullable=False, default=0)
    available = db.Column(db.Boolean, nullable=False, default=True)
    active = db.Column(db.Boolean, nullable=False, default=True)


class Offer(db.Model):
    __tablename__ = "offers"

    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(
        db.Integer, db.ForeignKey("work_requests.id"), nullable=False, index=True
    )
    contractor_id = db.Column(
        db.Integer, db.ForeignKey("contractors.id"), nullable=True, index=True
    )
    labor_hours = db.Column(db.Float, nullable=False, default=0)
    hourly_rate_sek = db.Column(db.Float, nullable=False, default=650)
    material_cost_sek = db.Column(db.Float, nullable=False, default=0)
    platform_fee_percent = db.Column(db.Float, nullable=False, default=10)
    subtotal_sek = db.Column(db.Float, nullable=False, default=0)
    platform_fee_sek = db.Column(db.Float, nullable=False, default=0)
    total_sek = db.Column(db.Float, nullable=False, default=0)
    status = db.Column(db.String(30), nullable=False, default="draft")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


def request_to_dict(item):
    return {
        "id": item.id,
        "customer_name": item.customer_name,
        "email": item.email,
        "phone": item.phone,
        "category": item.category,
        "description": item.description,
        "city": item.city,
        "postal_code": item.postal_code,
        "budget_sek": item.budget_sek,
        "urgency": item.urgency,
        "status": item.status,
        "created_at": item.created_at.isoformat() + "Z",
    }


def contractor_to_dict(item):
    return {
        "id": item.id,
        "company_name": item.company_name,
        "city": item.city,
        "categories": [c.strip() for c in item.categories.split(",") if c.strip()],
        "hourly_rate_sek": item.hourly_rate_sek,
        "rating": item.rating,
        "completed_jobs": item.completed_jobs,
        "available": item.available,
        "active": item.active,
    }


def offer_to_dict(item):
    return {
        "id": item.id,
        "request_id": item.request_id,
        "contractor_id": item.contractor_id,
        "labor_hours": item.labor_hours,
        "hourly_rate_sek": item.hourly_rate_sek,
        "material_cost_sek": item.material_cost_sek,
        "platform_fee_percent": item.platform_fee_percent,
        "subtotal_sek": item.subtotal_sek,
        "platform_fee_sek": item.platform_fee_sek,
        "total_sek": item.total_sek,
        "status": item.status,
        "created_at": item.created_at.isoformat() + "Z",
    }


def contractor_score(work_request, contractor):
    if not contractor.active:
        return 0, []

    score = 0
    reasons = []

    categories = {c.strip().lower() for c in contractor.categories.split(",") if c.strip()}
    if work_request.category.lower() in categories:
        score += 45
        reasons.append("category match")

    if contractor.city.strip().lower() == work_request.city.strip().lower():
        score += 25
        reasons.append("same city")

    if contractor.available:
        score += 10
        reasons.append("available now")

    rating_points = min(max(contractor.rating, 0), 5) / 5 * 15
    score += rating_points
    if contractor.rating:
        reasons.append(f"rating {contractor.rating:.1f}/5")

    experience_points = min(contractor.completed_jobs, 100) / 100 * 5
    score += experience_points
    if contractor.completed_jobs:
        reasons.append(f"{contractor.completed_jobs} completed jobs")

    return round(score, 1), reasons


@app.get("/health")
def health():
    return jsonify({"ok": True, "service": "constructionworkflowapp"})


@app.post("/projects")
def create_project():
    data = request.get_json(silent=True) or {}
    if "name" not in data:
        return jsonify({"error": "Name is required"}), 400

    new_project = Project(
        name=data["name"],
        description=data.get("description", ""),
    )
    db.session.add(new_project)
    db.session.commit()

    return jsonify(
        {
            "id": new_project.id,
            "name": new_project.name,
            "description": new_project.description,
        }
    ), 201


@app.get("/projects")
def list_projects():
    projects = Project.query.all()
    return jsonify(
        {
            "projects": [
                {
                    "id": p.id,
                    "name": p.name,
                    "description": p.description,
                }
                for p in projects
            ]
        }
    )


@app.post("/api/requests")
def create_work_request():
    data = request.get_json(silent=True) or {}
    required = ["customer_name", "category", "description", "city"]
    missing = [field for field in required if not str(data.get(field, "")).strip()]

    if missing:
        return jsonify({"error": "Missing required fields", "fields": missing}), 400

    work_request = WorkRequest(
        customer_name=str(data["customer_name"]).strip(),
        email=str(data.get("email", "")).strip() or None,
        phone=str(data.get("phone", "")).strip() or None,
        category=str(data["category"]).strip(),
        description=str(data["description"]).strip(),
        city=str(data["city"]).strip(),
        postal_code=str(data.get("postal_code", "")).strip() or None,
        budget_sek=float(data["budget_sek"]) if data.get("budget_sek") not in (None, "") else None,
        urgency=str(data.get("urgency", "flexible")).strip() or "flexible",
    )

    db.session.add(work_request)
    db.session.commit()

    return jsonify({"request": request_to_dict(work_request)}), 201


@app.get("/api/requests")
def list_work_requests():
    items = WorkRequest.query.order_by(WorkRequest.created_at.desc()).all()
    return jsonify({"requests": [request_to_dict(item) for item in items]})


@app.post("/api/contractors")
def create_contractor():
    data = request.get_json(silent=True) or {}
    required = ["company_name", "city", "categories"]
    missing = [field for field in required if not data.get(field)]

    if missing:
        return jsonify({"error": "Missing required fields", "fields": missing}), 400

    categories = data["categories"]
    if isinstance(categories, list):
        categories = ",".join(str(item).strip() for item in categories if str(item).strip())

    contractor = Contractor(
        company_name=str(data["company_name"]).strip(),
        city=str(data["city"]).strip(),
        categories=str(categories),
        hourly_rate_sek=float(data["hourly_rate_sek"]) if data.get("hourly_rate_sek") not in (None, "") else None,
        rating=float(data.get("rating", 0)),
        completed_jobs=int(data.get("completed_jobs", 0)),
        available=bool(data.get("available", True)),
        active=bool(data.get("active", True)),
    )

    db.session.add(contractor)
    db.session.commit()

    return jsonify({"contractor": contractor_to_dict(contractor)}), 201


@app.get("/api/contractors")
def list_contractors():
    items = Contractor.query.order_by(Contractor.company_name.asc()).all()
    return jsonify({"contractors": [contractor_to_dict(item) for item in items]})


@app.get("/api/requests/<int:request_id>/matches")
def match_contractors(request_id):
    work_request = db.session.get(WorkRequest, request_id)
    if not work_request:
        return jsonify({"error": "Request not found"}), 404

    ranked = []
    for contractor in Contractor.query.filter_by(active=True).all():
        score, reasons = contractor_score(work_request, contractor)
        if score > 0:
            ranked.append(
                {
                    "score": score,
                    "reasons": reasons,
                    "contractor": contractor_to_dict(contractor),
                }
            )

    ranked.sort(key=lambda item: item["score"], reverse=True)

    return jsonify(
        {
            "request": request_to_dict(work_request),
            "matches": ranked[:5],
        }
    )


@app.post("/api/requests/<int:request_id>/offers")
def create_offer(request_id):
    work_request = db.session.get(WorkRequest, request_id)
    if not work_request:
        return jsonify({"error": "Request not found"}), 404

    data = request.get_json(silent=True) or {}

    contractor_id = data.get("contractor_id")
    contractor = None
    if contractor_id:
        contractor = db.session.get(Contractor, int(contractor_id))
        if not contractor:
            return jsonify({"error": "Contractor not found"}), 404

    labor_hours = float(data.get("labor_hours", 0))
    material_cost = float(data.get("material_cost_sek", 0))
    default_rate = contractor.hourly_rate_sek if contractor and contractor.hourly_rate_sek else 650
    hourly_rate = float(data.get("hourly_rate_sek", default_rate))
    fee_percent = float(data.get("platform_fee_percent", 10))

    subtotal = max(0, labor_hours * hourly_rate + material_cost)
    fee = subtotal * fee_percent / 100
    total = subtotal + fee

    offer = Offer(
        request_id=work_request.id,
        contractor_id=contractor.id if contractor else None,
        labor_hours=labor_hours,
        hourly_rate_sek=hourly_rate,
        material_cost_sek=material_cost,
        platform_fee_percent=fee_percent,
        subtotal_sek=round(subtotal, 2),
        platform_fee_sek=round(fee, 2),
        total_sek=round(total, 2),
        status=str(data.get("status", "draft")),
    )

    db.session.add(offer)
    work_request.status = "quoted"
    db.session.commit()

    return jsonify({"offer": offer_to_dict(offer)}), 201


@app.get("/api/requests/<int:request_id>/offers")
def list_offers(request_id):
    work_request = db.session.get(WorkRequest, request_id)
    if not work_request:
        return jsonify({"error": "Request not found"}), 404

    offers = Offer.query.filter_by(request_id=request_id).order_by(Offer.created_at.desc()).all()
    return jsonify({"offers": [offer_to_dict(item) for item in offers]})


@app.post("/api/pilot/seed")
def seed_pilot_contractors():
    if Contractor.query.count() > 0:
        return jsonify(
            {
                "created": 0,
                "message": "Contractors already exist; seed skipped.",
            }
        )

    samples = [
        Contractor(
            company_name="Småland Byggpartner",
            city="Jönköping",
            categories="painting,carpentry,flooring,handyman",
            hourly_rate_sek=620,
            rating=4.8,
            completed_jobs=84,
            available=True,
        ),
        Contractor(
            company_name="Vätterstad Renovering",
            city="Jönköping",
            categories="bathroom,tiling,painting,carpentry",
            hourly_rate_sek=690,
            rating=4.7,
            completed_jobs=52,
            available=True,
        ),
        Contractor(
            company_name="Gislaved Servicebygg",
            city="Gislaved",
            categories="handyman,carpentry,kitchen,flooring",
            hourly_rate_sek=590,
            rating=4.5,
            completed_jobs=38,
            available=True,
        ),
    ]

    db.session.add_all(samples)
    db.session.commit()

    return jsonify(
        {
            "created": len(samples),
            "contractors": [contractor_to_dict(item) for item in samples],
        }
    ), 201


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(
        debug=os.environ.get("FLASK_DEBUG", "1") == "1",
        port=int(os.environ.get("PORT", "5000")),
    )
