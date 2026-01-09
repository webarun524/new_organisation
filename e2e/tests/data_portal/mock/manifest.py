# Mock OSDU manifest data for integration tests
# Template variable: DOMAIN

MANIFEST_DATA = {
    "executionContext": {
        "acl": {
            "owners": ["data.default.owners@osdu.DOMAIN"],
            "viewers": ["data.default.viewers@osdu.DOMAIN"],
        },
        "legal": {
            "status": "compliant",
            "legaltags": ["osdu-public-usa-dataset"],
            "otherRelevantDataCountries": ["US"],
        },
        "Payload": {
            "AppKey": "test-app",
            "data-partition-id": "osdu",
        },
        "manifest": {
            "kind": "osdu:wks:Manifest:1.0.0",
            "ReferenceData": [],
            "MasterData": [],
            "Data": {
                "WorkProduct": {
                    "kind": "osdu:wks:work-product--WorkProduct:1.0.0",
                    "acl": {
                        "owners": ["data.default.owners@osdu.DOMAIN"],
                        "viewers": ["data.default.viewers@osdu.DOMAIN"],
                    },
                    "legal": {
                        "legaltags": ["osdu-public-usa-dataset"],
                        "otherRelevantDataCountries": ["US"],
                    },
                    "data": {
                        "ResourceSecurityClassification": "osdu:reference-data--ResourceSecurityClassification:RESTRICTED:",
                        "Name": "1013_akm11_1978_comp.las",
                        "Description": "Well Log",
                        "Components": ["surrogate-key:wpc-1"],
                    },
                },
                "WorkProductComponents": [
                    {
                        "id": "surrogate-key:wpc-1",
                        "kind": "osdu:wks:work-product-component--WellLog:1.0.0",
                        "acl": {
                            "owners": ["data.default.owners@osdu.DOMAIN"],
                            "viewers": ["data.default.viewers@osdu.DOMAIN"],
                        },
                        "legal": {
                            "legaltags": ["osdu-public-usa-dataset"],
                            "otherRelevantDataCountries": ["US"],
                        },
                        "data": {
                            "ResourceSecurityClassification": "osdu:reference-data--ResourceSecurityClassification:RESTRICTED:",
                            "Name": "1013_akm11_1978_comp.las",
                            "Description": "Well Log",
                            "Datasets": ["surrogate-key:file-1"],
                            "WellboreID": "osdu:master-data--Wellbore:1013:",
                            "TopMeasuredDepth": 2182.0004,
                            "BottomMeasuredDepth": 2481,
                            "Curves": [
                                {
                                    "Mnemonic": "DEPT",
                                    "TopDepth": 2182,
                                    "BaseDepth": 2481,
                                    "DepthUnit": "osdu:reference-data--UnitOfMeasure:M:",
                                    "CurveUnit": "osdu:reference-data--UnitOfMeasure:M:",
                                },
                                {
                                    "Mnemonic": "GR",
                                    "TopDepth": 2182,
                                    "BaseDepth": 2481,
                                    "DepthUnit": "osdu:reference-data--UnitOfMeasure:M:",
                                    "CurveUnit": "osdu:reference-data--UnitOfMeasure:GAPI:",
                                },
                                {
                                    "Mnemonic": "DT",
                                    "TopDepth": 2182,
                                    "BaseDepth": 2481,
                                    "DepthUnit": "osdu:reference-data--UnitOfMeasure:M:",
                                    "CurveUnit": "osdu:reference-data--UnitOfMeasure:US%2FF:",
                                },
                                {
                                    "Mnemonic": "RHOB",
                                    "TopDepth": 2182,
                                    "BaseDepth": 2481,
                                    "DepthUnit": "osdu:reference-data--UnitOfMeasure:M:",
                                    "CurveUnit": "osdu:reference-data--UnitOfMeasure:G%2FC3:",
                                },
                                {
                                    "Mnemonic": "DRHO",
                                    "TopDepth": 2182,
                                    "BaseDepth": 2481,
                                    "DepthUnit": "osdu:reference-data--UnitOfMeasure:M:",
                                    "CurveUnit": "osdu:reference-data--UnitOfMeasure:G%2FC3:",
                                },
                                {
                                    "Mnemonic": "NPHI",
                                    "TopDepth": 2182,
                                    "BaseDepth": 2481,
                                    "DepthUnit": "osdu:reference-data--UnitOfMeasure:M:",
                                    "CurveUnit": "osdu:reference-data--UnitOfMeasure:V%2FV:",
                                },
                            ],
                        },
                    },
                ],
                "Datasets": [
                    {
                        "id": "surrogate-key:file-1",
                        "kind": "osdu:wks:dataset--File.Generic:1.0.0",
                        "acl": {
                            "owners": ["data.default.owners@osdu.DOMAIN"],
                            "viewers": ["data.default.viewers@osdu.DOMAIN"],
                        },
                        "legal": {
                            "legaltags": ["osdu-public-usa-dataset"],
                            "otherRelevantDataCountries": ["US"],
                        },
                        "data": {
                            "ResourceSecurityClassification": "osdu:reference-data--ResourceSecurityClassification:RESTRICTED:",
                            "SchemaFormatTypeID": "osdu:reference-data--SchemaFormatType:LAS2:",
                            "DatasetProperties": {
                                "FileSourceInfo": {
                                    "FileSource": "s3://osdu-artifacts-911600437027-us-east-1/r1/data/provided/well-logs/1013_akm11_1978_comp.las",
                                    "Name": "1013_akm11_1978_comp.las",
                                    "PreloadFilePath": "s3://osdu-artifacts-911600437027-us-east-1/r1/data/provided/well-logs/1013_akm11_1978_comp.las",
                                },
                            },
                        },
                    },
                ],
            },
        },
    },
}
