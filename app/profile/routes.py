# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import (Blueprint, render_template, g)
from sqlakeyset import get_page
from sqlalchemy import desc

from app.vulnerability.views.vulncode_db import (
    VulnViewTypesetPaginationObjectWrapper, )

from app import flash_error
from data.models import Vulnerability, Nvd
from data.models.nvd import default_nvd_view_options
from data.models.vulnerability import VulnerabilityState
from data.database import DEFAULT_DATABASE
from lib.utils import parse_pagination_param

bp = Blueprint("profile", __name__, url_prefix="/profile")
db = DEFAULT_DATABASE


# Create a catch all route for profile identifiers.
@bp.route("/proposals")
def view_proposals(vendor: str = None, profile: str = None):
    entries = db.session.query(Vulnerability, Nvd)
    entries = entries.filter(Vulnerability.creator == g.user)
    entries = entries.outerjoin(Vulnerability,
                                Nvd.cve_id == Vulnerability.cve_id)
    entries = entries.order_by(desc(Nvd.id))

    bookmarked_page = parse_pagination_param("proposal_p")
    per_page = 10
    entries_non_processed = entries.filter(~Vulnerability.state.in_(
        [VulnerabilityState.ARCHIVED, VulnerabilityState.PUBLISHED]))
    entries_full = entries_non_processed.options(default_nvd_view_options)
    proposal_vulns = get_page(entries_full, per_page, page=bookmarked_page)
    proposal_vulns = VulnViewTypesetPaginationObjectWrapper(
        proposal_vulns.paging)

    entries_processed = entries.filter(
        Vulnerability.state.in_(
            [VulnerabilityState.ARCHIVED, VulnerabilityState.PUBLISHED]))
    bookmarked_page_processed = parse_pagination_param("proposal_processed_p")
    entries_processed_full = entries_processed.options(
        default_nvd_view_options)
    proposal_vulns_processed = get_page(entries_processed_full,
                                        per_page,
                                        page=bookmarked_page_processed)
    proposal_vulns_processed = VulnViewTypesetPaginationObjectWrapper(
        proposal_vulns_processed.paging)

    return render_template(
        "profile/proposals_view.html",
        proposal_vulns=proposal_vulns,
        proposal_vulns_processed=proposal_vulns_processed,
    )
