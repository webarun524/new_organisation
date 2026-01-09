/* Setup Data Portal resources by SSO Provider */

resource "aws_iam_policy" "custom_fulfillment_policy" {
  name        = "${var.resource_prefix}-custom-fulfillment-policy"
  description = "Custom fulfillment policy for Data Portal"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cloudformation:CreateChangeSet",
        "cloudformation:CreateStack",
        "cloudformation:DeleteStack",
        "cloudformation:DescribeStacks",
        "cloudformation:ListStacks",
        "cloudformation:UpdateStack",
        "cloudformation:ListStackResources",
        "codebuild:BatchGetBuilds",
        "codebuild:CreateProject",
        "codebuild:DeleteProject",
        "codebuild:UpdateProject",
        "codepipeline:CreatePipeline",
        "codepipeline:DeletePipeline",
        "codepipeline:GetPipeline",
        "codepipeline:GetPipelineState",
        "codepipeline:ListPipelines",
        "codepipeline:RetryStageExecution",
        "codepipeline:TagResource",
        "codepipeline:UpdatePipeline",
        "ec2:CreateKeyPair",
        "ec2:DescribeKeyPairs",
        "ec2:DescribeVpcs",
        "ecs:RunTask",
        "ec2:CreateVpc",
        "ec2:DeleteVpc",
        "ec2:ModifyVpcAttribute",
        "ec2:CreateSubnet",
        "ec2:DeleteSubnet",
        "ec2:DescribeSubnets",
        "ec2:CreateInternetGateway",
        "ec2:AttachInternetGateway",
        "ec2:DetachInternetGateway",
        "ec2:DeleteInternetGateway",
        "ec2:DescribeRouteTables",
        "ec2:CreateRoute",
        "ec2:CreateTransitGateway",
        "ec2:DeleteTransitGateway",
        "ec2:DescribeTransitGateways",
        "ec2:CreateTransitGatewayVpcAttachment",
        "ec2:DeleteTransitGatewayVpcAttachment",
        "ec2:DescribeTransitGatewayVpcAttachments",
        "ec2:DescribeTransitGatewayRouteTables",
        "ec2:DescribeTransitGatewayAttachments",
        "ec2:CreateTransitGatewayRoute",
        "ec2:AllocateAddress",
        "ec2:ReleaseAddress",
        "ec2:DescribeAddresses",
        "ec2:CreateNatGateway",
        "ec2:DeleteNatGateway",
        "ec2:DescribeNatGateways",
        "ec2:CreateRouteTable",
        "ec2:DeleteRouteTable",
        "ec2:AssociateRouteTable",
        "ec2:DisassociateRouteTable",
        "ec2:CreateTags",
        "eks:*",
        "events:PutEvents",
        "iam:AttachRolePolicy",
        "iam:CreatePolicy",
        "iam:CreateRole",
        "iam:DeletePolicy",
        "iam:DeleteRole",
        "iam:DetachRolePolicy",
        "iam:GetPolicy",
        "iam:GetPolicyVersion",
        "iam:GetRole",
        "iam:PassRole",
        "iam:GetRolePolicy",
        "iam:ListPolicyVersions",
        "iam:PutRolePolicy",
        "iam:TagRole",
        "lambda:CreateFunction",
        "lambda:DeleteFunction",
        "lambda:GetFunction",
        "lambda:TagResource",
        "lambda:UpdateFunctionConfiguration",
        "lambda:ListTags",
        "resource-groups:*",
        "route53:ChangeTagsForResource",
        "route53:CreateHostedZone",
        "route53:DeleteHostedZone",
        "route53:GetChange",
        "route53:GetHostedZone",
        "route53:ListHostedZones",
        "route53:ListQueryLoggingConfigs",
        "route53:ListTagsForResource",
        "route53:ChangeResourceRecordSets",
        "route53:ListResourceRecordSets",
        "route53profiles:CreateProfile",
        "route53profiles:AssociateResourceToProfile",
        "route53profiles:AssociateProfile",
        "s3:CreateBucket",
        "s3:DeleteObject",
        "s3:DeleteObjectVersion",
        "s3:DeleteBucket",
        "s3:GetBucketPolicy",
        "s3:GetBucketVersioning",
        "s3:List*",
        "s3:Put*",
        "servicequotas:GetServiceQuota",
        "ssm:DeleteParameter",
        "ssm:DeleteParameters",
        "ssm:GetParameter",
        "ssm:GetParameters",
        "ssm:PutParameter",
        "ssm:AddTagsToResource",
        "states:CreateStateMachine",
        "states:DescribeStateMachine",
        "states:DeleteStateMachine",
        "states:TagResource",
        "sts:GetCallerIdentity",
        "cognito-idp:ListUserPools",
        "cognito-idp:ListUserPoolClients",
        "cognito-idp:DescribeUserPoolClient",
        "cognito-idp:CreateUserPoolClient",
        "cognito-idp:DescribeUserPool",
        "secretsmanager:CreateSecret",
        "secretsmanager:DeleteSecret",
        "secretsmanager:UpdateSecret",
        "secretsmanager:GetSecretValue",
        "sqs:GetQueueAttributes",
        "sqs:GetQueueUrl",
        "acm-pca:DescribeCertificateAuthority",
        "acm-pca:CreateCertificateAuthority",
        "acm-pca:UpdateCertificateAuthority",
        "acm-pca:DeleteCertificateAuthority",
        "acm-pca:GetCertificateAuthorityCsr",
        "acm-pca:IssueCertificate",
        "acm-pca:GetCertificate",
        "acm-pca:ImportCertificateAuthorityCertificate",
        "ram:CreatePermission",
        "ram:CreateResourceShare"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "iam:PassRole",
        "iam:CreateServiceLinkedRole",
        "sts:AssumeRole"
      ],
      "Resource": [
        "arn:aws:iam::*:role/OSDUR2DynamodbTableScalingRole-*",
        "arn:aws:iam::*:role/OSDUR2EcsAutoScalingRole-*",
        "arn:aws:iam::*:role/OSDUR2EcsTaskExecutionRole-*",
        "arn:aws:iam::*:role/OSDUR2EntitlementsLambdaRole-*",
        "arn:aws:iam::*:role/OSDUR2PipelineDeployRole-*",
        "arn:aws:iam::*:role/OSDUR2PipelineDestroyRole-*",
        "arn:aws:iam::*:role/aws-service-role/dynamodb.application-autoscaling.amazonaws.com/*",
        "arn:aws:iam::*:role/aws-service-role/ecs.amazonaws.com/*",
        "arn:aws:iam::*:role/aws-service-role/ecs.application-autoscaling.amazonaws.com/*",
        "arn:aws:iam::*:role/aws-service-role/elasticache.amazonaws.com/*",
        "arn:aws:iam::*:role/aws-service-role/elasticloadbalancing.amazonaws.com/*",
        "arn:aws:iam::*:role/aws-service-role/es.amazonaws.com/*",
        "arn:aws:iam::*:role/aws-service-role/transitgateway.amazonaws.com/*"
      ]
    },
    {
      "Sid": "GetOsduPostmanEnv",
      "Effect": "Allow",
      "Action": ["s3:GetObject"],
      "Resource": ["arn:aws:s3:::osduonaws-artifacts/*"]
    },
    {
      "Effect": "Allow",
      "Action": ["iam:SimulatePrincipalPolicy"],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": ["route53profiles:*", "ram:*", "acm-pca:*"],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "kms:CreateKey",
        "kms:PutKeyPolicy",
        "kms:TagResource",
        "kms:EnableKeyRotation",
        "kms:ScheduleKeyDeletion",
        "kms:DescribeKey",
        "kms:CancelKeyDeletion",
        "kms:CreateAlias"
      ],
      "Resource": "*"
    }
  ]
}
EOF

  tags = local.merged_tags
}

data "aws_iam_policy_document" "custom_fulfillment_trust" {
  version = "2012-10-17"

  dynamic "statement" {
    for_each = var.trusted_accounts
    content {
      effect = "Allow"

      principals {
        type        = "AWS"
        identifiers = ["arn:aws:iam::${statement.value}:root"]
      }

      actions = ["sts:AssumeRole"]

      condition {
        test     = "StringLike"
        variable = "sts:ExternalId"
        values   = ["${var.organization_id}-*"]
      }
    }
  }
}

resource "aws_iam_role" "custom_fulfillment_role" {
  name               = "${var.resource_prefix}-custom-fulfillment-role"
  assume_role_policy = data.aws_iam_policy_document.custom_fulfillment_trust.json
  tags               = local.merged_tags
}

resource "aws_iam_role_policy_attachment" "custom_policy_attach" {
  role       = aws_iam_role.custom_fulfillment_role.name
  policy_arn = aws_iam_policy.custom_fulfillment_policy.arn
}

resource "aws_iam_role_policy_attachment" "eks_cluster_policy_attach" {
  role       = aws_iam_role.custom_fulfillment_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
}

resource "aws_iam_role_policy_attachment" "eks_local_outpost_policy_attach" {
  role       = aws_iam_role.custom_fulfillment_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSLocalOutpostClusterPolicy"
}


/* Cognito, SSM, SM cross access role */

resource "aws_iam_role" "cognito_secrets_ssm_cross_role" {
  name = "${var.resource_prefix}-cognito-secrets-ssm-cross-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = "sts:AssumeRole"

      Principal = {
        AWS = [
          for account_id in var.trusted_accounts :
          "arn:aws:iam::${account_id}:root"
        ]
      }
    }]
  })

  tags = local.merged_tags
}

resource "aws_iam_policy" "cognito_secrets_ssm_cross_policy" {
  name = "${var.resource_prefix}-cognito-secrets-ssm-cross-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid      = "CrossAccessReadSecrets"
        Effect   = "Allow"
        Action   = "secretsmanager:GetSecretValue"
        Resource = "arn:aws:secretsmanager:${var.aws_region}:*:secret:*"
      },
      {
        Sid    = "CrossAccessReadSSMParameters"
        Effect = "Allow"
        Action = [
          "ssm:GetParameter",
          "ssm:GetParameters",
          "ssm:GetParametersByPath"
        ]
        Resource = "arn:aws:ssm:${var.aws_region}:*:parameter/*"
      },
      {
        Sid      = "CrossAccessSetPermanentCognitoPassword"
        Effect   = "Allow"
        Action   = [
          "cognito-idp:AdminSetUserPassword",
          "cognito-idp:AdminGetUser"
        ]
        Resource = "arn:aws:cognito-idp:${var.aws_region}:*:userpool/*"
      }
    ]
  })

  tags = local.merged_tags
}

resource "aws_iam_role_policy_attachment" "attach_cognito_secrets_ssm_cross_policy" {
  role       = aws_iam_role.cognito_secrets_ssm_cross_role.name
  policy_arn = aws_iam_policy.cognito_secrets_ssm_cross_policy.arn
}
