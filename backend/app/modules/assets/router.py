from fastapi import APIRouter
from app.modules.assets.service import AssetService
from app.modules.assets.schema import AssetProfileResponse, AssetSummaryResponse, TimelineEvent, AssetListResponse
from app.shared.responses import SuccessResponse
from typing import List

router = APIRouter(prefix="/assets", tags=["assets"])

@router.get("", response_model=SuccessResponse[AssetListResponse], summary="List Assets")
def get_all_assets():
    service = AssetService()
    assets = service.get_all_assets()
    return SuccessResponse(message="Assets retrieved", data={"assets": assets})

@router.get("/{asset_id}", response_model=SuccessResponse[AssetProfileResponse], summary="Get Asset Profile")
def get_asset_profile(asset_id: str):
    service = AssetService()
    profile = service.get_asset_profile(asset_id)
    return SuccessResponse(message="Asset profile retrieved", data=profile)

@router.get("/{asset_id}/timeline", response_model=SuccessResponse[List[TimelineEvent]], summary="Get Asset Timeline")
def get_asset_timeline(asset_id: str):
    service = AssetService()
    timeline = service.get_asset_timeline(asset_id)
    return SuccessResponse(message="Asset timeline retrieved", data=timeline)

@router.get("/{asset_id}/documents", response_model=SuccessResponse[list], summary="Get Connected Documents")
def get_asset_documents(asset_id: str):
    service = AssetService()
    docs = service.get_asset_documents(asset_id)
    return SuccessResponse(message="Asset documents retrieved", data=docs)

@router.get("/{asset_id}/relationships", response_model=SuccessResponse[dict], summary="Get Raw Relationships")
def get_asset_relationships(asset_id: str):
    service = AssetService()
    rels = service.get_asset_relationships(asset_id)
    return SuccessResponse(message="Asset relationships retrieved", data=rels)

@router.get("/{asset_id}/summary", response_model=SuccessResponse[AssetSummaryResponse], summary="Get AI Summary")
def get_asset_summary(asset_id: str):
    service = AssetService()
    summary = service.generate_ai_summary(asset_id)
    return SuccessResponse(message="Asset summary generated", data={"summary": summary})
