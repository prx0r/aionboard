"""AI Onboard pilot package."""

from .crm import (
    SCHEMA_VERSION,
    add_contact,
    assert_contact_allowed,
    connect,
    get_prospect,
    import_prospects,
    init_db,
    parse_region,
    record_contact_attempt,
    record_tps_check,
)
from .demo import run_demo
from .handover import generate_handover, write_handover
from .installs import (
    OPTIONAL_TASKS,
    REQUIRED_TASKS,
    STATUSES,
    create_install,
    get_install,
    is_complete,
    set_task,
)
from .security import approve_action, assert_customer_isolation, execute_outbound, scan_text
from .website import canonical_domain, render_site, write_site

__all__ = [
    "SCHEMA_VERSION",
    "OPTIONAL_TASKS",
    "REQUIRED_TASKS",
    "STATUSES",
    "add_contact",
    "approve_action",
    "assert_contact_allowed",
    "assert_customer_isolation",
    "canonical_domain",
    "connect",
    "create_install",
    "execute_outbound",
    "generate_handover",
    "get_install",
    "get_prospect",
    "import_prospects",
    "init_db",
    "is_complete",
    "parse_region",
    "record_contact_attempt",
    "record_tps_check",
    "render_site",
    "run_demo",
    "scan_text",
    "set_task",
    "write_handover",
    "write_site",
]

__version__ = "0.1.0"
