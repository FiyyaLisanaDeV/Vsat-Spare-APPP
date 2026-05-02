"""
Seed data awal untuk sistem VSAT Spare Stock Management.
Jalankan via: docker exec backend python -m app.db.seed
Script ini idempoten — aman dijalankan berulang kali.
"""
import sys
import os

# Pastikan path benar saat dijalankan langsung
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.db.base import SessionLocal
from app.models.user import User, UserRole
from app.models.service_point import ServicePoint, ServicePointType
from app.models.item import ItemType, ItemCategory, SpareItem
from app.core.security import hash_password
from app.utils.logger import logger


def seed():
    db = SessionLocal()
    try:
        logger.info("Memulai seed data awal...")

        # ── Admin Awal ────────────────────────────────────────────────────
        admin = db.query(User).filter(User.email == "admin@jakarta.vsat").first()
        if not admin:
            admin = User(
                name="Administrator Jakarta",
                email="admin@jakarta.vsat",
                password_hash=hash_password("Admin123!"),
                role=UserRole.admin_jakarta,
                service_point_id=None,
                is_active=True,
                force_password_change=True,
            )
            db.add(admin)
            db.flush()
            logger.info("Admin awal dibuat: admin@jakarta.vsat")
        else:
            logger.info("Admin awal sudah ada, skip.")

        # ── Service Points ────────────────────────────────────────────────
        service_points_data = [
            {
                "name": "Jakarta",
                "type": ServicePointType.service_representative,
                "city": "Jakarta",
                "province": "DKI Jakarta",
                "pic_name": "PIC Jakarta",
                "pic_phone": "08111000001",
                "pic_email": "pic.jakarta@vsat.local",
            },
            {
                "name": "Kendari",
                "type": ServicePointType.service_representative,
                "city": "Kendari",
                "province": "Sulawesi Tenggara",
                "pic_name": "PIC Kendari",
                "pic_phone": "08111000002",
                "pic_email": "pic.kendari@vsat.local",
            },
            {
                "name": "Makassar",
                "type": ServicePointType.subcon,
                "city": "Makassar",
                "province": "Sulawesi Selatan",
                "pic_name": "PIC Makassar",
                "pic_phone": "08111000003",
                "pic_email": "pic.makassar@vsat.local",
            },
        ]

        for sp_data in service_points_data:
            sp = db.query(ServicePoint).filter(ServicePoint.name == sp_data["name"]).first()
            if not sp:
                sp = ServicePoint(**sp_data)
                db.add(sp)
                logger.info(f"Service Point dibuat: {sp_data['name']}")
        db.flush()

        # ── Item Types ────────────────────────────────────────────────────
        type_map = {}
        item_types_data = ["RF Equipment", "Modem & Controller", "Aksesoris"]
        for type_name in item_types_data:
            it = db.query(ItemType).filter(ItemType.name == type_name).first()
            if not it:
                it = ItemType(name=type_name, is_active=True)
                db.add(it)
                db.flush()
                logger.info(f"Item Type dibuat: {type_name}")
            type_map[type_name] = it

        # ── Item Categories ───────────────────────────────────────────────
        category_map = {}
        categories_data = {
            "RF Equipment": ["Outdoor Unit", "Indoor Unit"],
            "Modem & Controller": ["Modem", "Power Supply"],
            "Aksesoris": ["Konektor", "Kabel"],
        }
        for type_name, cats in categories_data.items():
            parent_type = type_map[type_name]
            for cat_name in cats:
                cat = (
                    db.query(ItemCategory)
                    .filter(
                        ItemCategory.type_id == parent_type.id,
                        ItemCategory.name == cat_name,
                    )
                    .first()
                )
                if not cat:
                    cat = ItemCategory(
                        type_id=parent_type.id, name=cat_name, is_active=True
                    )
                    db.add(cat)
                    db.flush()
                    logger.info(f"Item Category dibuat: {cat_name} [{type_name}]")
                category_map[f"{type_name}:{cat_name}"] = cat

        # ── Spare Items ───────────────────────────────────────────────────
        spare_items_data = [
            {
                "sku": "BUC-CB-001",
                "name": "BUC C-Band",
                "type_name": "RF Equipment",
                "category_name": "Outdoor Unit",
                "unit": "unit",
                "min_stock": 2,
            },
            {
                "sku": "LNB-CB-001",
                "name": "LNB C-Band",
                "type_name": "RF Equipment",
                "category_name": "Outdoor Unit",
                "unit": "unit",
                "min_stock": 2,
            },
            {
                "sku": "MDM-HX90-001",
                "name": "Modem HX90",
                "type_name": "Modem & Controller",
                "category_name": "Modem",
                "unit": "unit",
                "min_stock": 1,
            },
            {
                "sku": "PWR-48V-001",
                "name": "Adaptor 48V",
                "type_name": "Modem & Controller",
                "category_name": "Power Supply",
                "unit": "pcs",
                "min_stock": 3,
            },
            {
                "sku": "KNK-IFL-001",
                "name": "Konektor IFL",
                "type_name": "Aksesoris",
                "category_name": "Konektor",
                "unit": "pcs",
                "min_stock": 10,
            },
        ]

        for item_data in spare_items_data:
            existing = (
                db.query(SpareItem).filter(SpareItem.sku == item_data["sku"]).first()
            )
            if not existing:
                type_obj = type_map[item_data["type_name"]]
                cat_key = f"{item_data['type_name']}:{item_data['category_name']}"
                cat_obj = category_map[cat_key]
                spare = SpareItem(
                    sku=item_data["sku"],
                    name=item_data["name"],
                    type_id=type_obj.id,
                    category_id=cat_obj.id,
                    unit=item_data["unit"],
                    min_stock=item_data["min_stock"],
                    requires_serial=False,
                    is_active=True,
                )
                db.add(spare)
                logger.info(f"Spare Item dibuat: {item_data['sku']} - {item_data['name']}")

        db.commit()
        logger.info("Seed data selesai. Sistem siap digunakan.")

    except Exception as e:
        db.rollback()
        logger.error(f"Seed gagal: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
