# the updated prompt

sql_prompt = """
    A database has the following schema with tables and relationships. 

You are a SQL expert and based on user prompt , you should generate correct SQL to answer the user prompt. Use Joins where necessary.

Please give only one SQL as output.

The user has entered {user_prompt}
/****** Object:  Table [dbo].[Segments]    Script Date: 21-05-2024 15:14:22 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Segments](
	[segment_id] [int] NOT NULL,
	[name] [varchar](255) NOT NULL,
	[description] [text] NULL,
PRIMARY KEY CLUSTERED 
(
	[segment_id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

/****** Object:  Table [dbo].[Lines_of_Business]    Script Date: 21-05-2024 15:14:36 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Lines_of_Business](
	[lob_id] [int] NOT NULL,
	[segment_id] [int] NULL,
	[name] [varchar](255) NOT NULL,
	[description] [text] NULL,
PRIMARY KEY CLUSTERED 
(
	[lob_id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

ALTER TABLE [dbo].[Lines_of_Business]  WITH CHECK ADD FOREIGN KEY([segment_id])
REFERENCES [dbo].[Segments] ([segment_id])
GO


/****** Object:  Table [dbo].[Coverage_Types]    Script Date: 21-05-2024 15:14:57 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Coverage_Types](
	[coverage_type_id] [int] NOT NULL,
	[line_of_business] [int] NOT NULL,
	[description] [text] NULL,
PRIMARY KEY CLUSTERED 
(
	[coverage_type_id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

ALTER TABLE [dbo].[Coverage_Types]  WITH CHECK ADD FOREIGN KEY([line_of_business])
REFERENCES [dbo].[Lines_of_Business] ([lob_id])
GO

/****** Object:  Table [dbo].[Coverages]    Script Date: 21-05-2024 15:15:24 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO






CREATE TABLE [dbo].[PolicyDetails](
	PolicyID [int] IDENTITY(1,1) NOT NULL,
	[pkAgency] [int] not NULL,
	[LineofBusiness] [varchar](256) NULL,
	[PolicyNumber] [varchar](25) NULL,
	[TermNumber] [varchar](10) NULL,
	[EffectiveDate] [datetime] NULL,
	[ExpirationDate] [datetime] NULL,
	[AccountNumber] [varchar](25) NULL,
	[New_Renewal] [char](1) NULL,
	[Addressline1] [varchar](126) NULL,
	[City] [varchar](126) NULL,
	[County] [varchar](126) NULL,
	[zipcode] [varchar](5) NULL,
	[State] [varchar](25) NULL,
	[SegmentName] [varchar](126) NULL,
	[Installment_Term] [char](3) NULL,
	[NumberOfInstallments] [varchar](50) NULL,
	[PolicyStatus] [varchar](50) NULL,
	[Premium] decimal(32,2) null,
	[TotalPremiumPaid] decimal(32,2) null,
	[PremiumBalance] decimal(32,2) null,
	[PremiumDueDate] datetime null
PRIMARY KEY CLUSTERED 
(
	policyid ASC
),
FOREIGN KEY (PKAGENCY) REFERENCES Agency (pkagency),
FOREIGN KEY (AccountNumber) REFERENCES Customer (account_number)
) ON [PRIMARY]
;


CREATE TABLE [dbo].[Coverages](
	[coverage_id] [int] NOT NULL,
	[policy_id] [int] NOT NULL,
	[coverage_type_id] [int] NOT NULL,
	[limit] [decimal](32, 2) NULL,
	[deductible] [decimal](32, 2) NULL,
PRIMARY KEY CLUSTERED 
(
	[coverage_id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[Coverages]  WITH CHECK ADD FOREIGN KEY([coverage_type_id])
REFERENCES [dbo].[Coverage_Types] ([coverage_type_id])
GO

ALTER TABLE [dbo].[Coverages]  WITH CHECK ADD FOREIGN KEY([policy_id])
REFERENCES [dbo].[PolicyDetails] ([PolicyID])
GO



CREATE TABLE [dbo].[ClaimDetails](
	ClaimID [int] IDENTITY(1,1) NOT NULL,
	PolicyID [int] not NULL,
	[LineofBusiness] [varchar](256) NULL,
	[PolicyNumber] [varchar](25) NULL,
	[TermNumber] [varchar](10) NULL,
	[EffectiveDate] [datetime] NULL,
	[ExpirationDate] [datetime] NULL,
	[LossDate] datetime null,
	[AssignedAdjuster] [varchar](256) NULL,
	[New_Renewal] [char](1) NULL,
	[LossAddressline1] [varchar](126) NULL,
	[LossCity] [varchar](126) NULL,
	[LossCounty] [varchar](126) NULL,
	[Losszipcode] [varchar](5) NULL,
	[LossState] [varchar](25) NULL,
	[IncurredLosses] decimal(32,2) null,
	[TotalExpenses] decimal(32,2) null,
	[OutstandingReserves] decimal(32,2) null
PRIMARY KEY CLUSTERED 
(
	ClaimID ASC
),
FOREIGN KEY (policyid) REFERENCES policydetails (policyid),

) ON [PRIMARY];


CREATE TABLE Customer (
    account_number INT NOT NULL,
    customer_name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    phone_number VARCHAR(15) NOT NULL,
    date_of_birth DATE NOT NULL,
    PRIMARY KEY (account_number)
);
        
        
    """