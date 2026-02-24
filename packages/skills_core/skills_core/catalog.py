"""
Deterministic catalog generation
"""
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import List
from skills_core.types import Catalog, CatalogEntry, SkillMetadata
from skills_core.loader import discover_skills


def generate_catalog(skills_dir: Path, output_path: Path) -> Catalog:
    """
    Generate skills catalog deterministically
    
    Args:
        skills_dir: Path to skills directory
        output_path: Path to write catalog.json
        
    Returns:
        Generated Catalog object
    """
    # Discover all skills
    skills = discover_skills(skills_dir)
    
    # Convert to catalog entries
    entries = []
    for skill in skills:
        entry = CatalogEntry(
            id=skill.id,
            name=skill.name,
            version=skill.version,
            description=skill.description,
            tags=skill.tags,
            safety_level=skill.safety.level,
            permissions=skill.permissions,
            dspy_module=skill.dspy.module,
            owner=skill.owner
        )
        entries.append(entry)
    
    # Sort by ID for deterministic output
    entries.sort(key=lambda e: e.id)
    
    # Create catalog
    catalog = Catalog(
        version="1.0",
        generated_at=datetime.now(timezone.utc).isoformat(),
        skills=entries
    )
    
    # Write to file with deterministic formatting
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(
            catalog.model_dump(),
            f,
            indent=2,
            sort_keys=True,
            ensure_ascii=False
        )
        f.write('\n')  # Ensure file ends with newline
    
    return catalog


def load_catalog(catalog_path: Path) -> Catalog:
    """
    Load catalog from file
    
    Args:
        catalog_path: Path to catalog.json
        
    Returns:
        Catalog object
    """
    with open(catalog_path, 'r') as f:
        data = json.load(f)
    
    return Catalog(**data)


def compare_catalogs(catalog1: Catalog, catalog2: Catalog) -> bool:
    """
    Compare two catalogs for equality (ignoring generated_at timestamp)
    
    Args:
        catalog1: First catalog
        catalog2: Second catalog
        
    Returns:
        True if catalogs are equivalent
    """
    # Compare versions
    if catalog1.version != catalog2.version:
        return False
    
    # Compare skill lists (sorting by ID)
    skills1 = sorted([s.model_dump() for s in catalog1.skills], key=lambda s: s['id'])
    skills2 = sorted([s.model_dump() for s in catalog2.skills], key=lambda s: s['id'])
    
    # Remove owner fields if they're None for comparison
    for s in skills1 + skills2:
        if s.get('owner') is None:
            s.pop('owner', None)
    
    return skills1 == skills2
