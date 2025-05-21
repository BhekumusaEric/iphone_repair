#!/usr/bin/env python3
"""
InheritanceSupport.py - Support for inherited device access

This module provides guidance and support for users who have inherited devices
but cannot access them due to activation lock or unknown credentials. It focuses
on legitimate inheritance cases and provides guidance on official processes.

NOTE: This module does NOT attempt to bypass security measures. It provides
guidance on legitimate processes for device inheritance.
"""

import os
import sys
import time
import logging
import tempfile
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any, Union, Set

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import local modules
from .DiagnosticTool import DeviceInfo

class InheritanceSupportResult(Enum):
    """Enumeration of inheritance support results"""
    DOCUMENTATION_GENERATED = 1
    GUIDANCE_PROVIDED = 2
    APPLE_SUPPORT_CONTACT = 3
    LIMITED_DOCUMENTATION_SUPPORT = 4
    ALTERNATIVE_OPTIONS_PROVIDED = 5
    NOT_APPLICABLE = 6

class InheritanceSupport:
    """Support for inherited device access"""

    def __init__(self, device_info: DeviceInfo = None, debug: bool = False):
        """
        Initialize inheritance support

        Args:
            device_info: Information about the device (optional)
            debug: Whether to enable debug logging
        """
        self.device_info = device_info
        self.debug = debug
        self.logs = []

        if debug:
            logger.setLevel(logging.DEBUG)

    def log(self, message: str) -> None:
        """Add a message to the logs"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.logs.append(log_entry)
        logger.info(message)

    def provide_inheritance_guidance(self) -> InheritanceSupportResult:
        """
        Provide guidance for inherited device access

        Returns:
            InheritanceSupportResult: The result of the guidance
        """
        self.log("Starting inheritance support guidance")
        self.log("This process will help with legitimate inheritance cases")

        # Provide general guidance
        self.log("\nFor inherited devices with activation lock or unknown credentials:")
        self.log("1. Apple has an official process for handling inherited devices")
        self.log("2. You will need documentation to prove legitimate inheritance")
        self.log("3. This tool can help prepare the necessary documentation")

        # Return guidance result
        return InheritanceSupportResult.GUIDANCE_PROVIDED

    def generate_documentation_templates(self, output_dir: str = None) -> Dict[str, str]:
        """
        Generate documentation templates for inheritance claims

        Args:
            output_dir: Directory to save templates (optional)

        Returns:
            Dict[str, str]: Dictionary of template paths
        """
        self.log("Generating documentation templates for inheritance claims")

        # Create temporary directory if output_dir not provided
        if output_dir is None:
            output_dir = tempfile.mkdtemp(prefix="inheritance_docs_")
            self.log(f"Created temporary directory: {output_dir}")
        else:
            os.makedirs(output_dir, exist_ok=True)
            self.log(f"Using directory: {output_dir}")

        # Define templates
        templates = {
            "inheritance_letter": self._generate_inheritance_letter_template(output_dir),
            "statutory_declaration": self._generate_statutory_declaration_template(output_dir),
            "apple_support_request": self._generate_apple_support_request_template(output_dir),
            "checklist": self._generate_documentation_checklist(output_dir)
        }

        self.log(f"Generated {len(templates)} documentation templates")
        for name, path in templates.items():
            self.log(f"- {name}: {path}")

        return templates

    def _generate_inheritance_letter_template(self, output_dir: str) -> str:
        """
        Generate inheritance letter template

        Args:
            output_dir: Directory to save template

        Returns:
            str: Path to generated template
        """
        template_path = os.path.join(output_dir, "inheritance_letter_template.txt")

        with open(template_path, "w") as f:
            f.write("INHERITANCE LETTER TEMPLATE\n")
            f.write("===========================\n\n")
            f.write("Date: [CURRENT DATE]\n\n")
            f.write("To Whom It May Concern:\n\n")
            f.write("I, [YOUR FULL NAME], am writing to confirm that I have inherited an Apple device from [DECEASED PERSON'S FULL NAME], who passed away on [DATE OF DEATH].\n\n")
            f.write("Device Details:\n")
            f.write("- Device Type: [iPhone/iPad/etc.]\n")
            f.write("- Model: [MODEL NUMBER, e.g., iPhone XS]\n")
            f.write("- Serial Number: [SERIAL NUMBER]\n")
            f.write("- IMEI (if applicable): [IMEI NUMBER]\n\n")
            f.write("My relationship to the deceased was [RELATIONSHIP, e.g., son, daughter, spouse].\n\n")
            f.write("I am requesting assistance in accessing this device as I am unable to provide the Apple ID password previously used by the deceased. I have attached the following documentation to support my request:\n\n")
            f.write("1. Death Certificate\n")
            f.write("2. Proof of Inheritance (Will, Probate Document, etc.)\n")
            f.write("3. Proof of Identity (My Government-issued ID)\n")
            f.write("4. Proof of Relationship to the Deceased\n")
            f.write("5. Proof of Purchase (if available)\n\n")
            f.write("I understand that Apple takes security and privacy very seriously, and I appreciate your assistance in this sensitive matter.\n\n")
            f.write("Sincerely,\n\n")
            f.write("[YOUR FULL NAME]\n")
            f.write("[YOUR CONTACT INFORMATION]\n")
            f.write("[YOUR EMAIL ADDRESS]\n")
            f.write("[YOUR PHONE NUMBER]\n")

        return template_path

    def _generate_statutory_declaration_template(self, output_dir: str) -> str:
        """
        Generate statutory declaration template

        Args:
            output_dir: Directory to save template

        Returns:
            str: Path to generated template
        """
        template_path = os.path.join(output_dir, "statutory_declaration_template.txt")

        with open(template_path, "w") as f:
            f.write("STATUTORY DECLARATION TEMPLATE\n")
            f.write("==============================\n\n")
            f.write("STATUTORY DECLARATION\n\n")
            f.write("I, [YOUR FULL NAME], of [YOUR ADDRESS], do solemnly and sincerely declare that:\n\n")
            f.write("1. I am the [RELATIONSHIP] of the late [DECEASED PERSON'S FULL NAME], who passed away on [DATE OF DEATH].\n\n")
            f.write("2. The deceased was the owner of an Apple [DEVICE TYPE], Model [MODEL NUMBER], Serial Number [SERIAL NUMBER], IMEI [IMEI NUMBER].\n\n")
            f.write("3. I have inherited this device as per [REFERENCE TO WILL/PROBATE/INHERITANCE DOCUMENT].\n\n")
            f.write("4. I do not have access to the deceased's Apple ID or password.\n\n")
            f.write("5. I am seeking to gain access to this device for legitimate purposes as the rightful inheritor.\n\n")
            f.write("6. All information provided in this declaration and accompanying documents is true and correct to the best of my knowledge.\n\n")
            f.write("And I make this solemn declaration conscientiously believing the same to be true and by virtue of the provisions of the [RELEVANT STATUTORY DECLARATIONS ACT IN YOUR JURISDICTION].\n\n")
            f.write("Declared at [LOCATION] on [DATE]\n\n")
            f.write("_______________________\n")
            f.write("[YOUR FULL NAME]\n\n")
            f.write("Before me,\n\n")
            f.write("_______________________\n")
            f.write("[NAME OF WITNESS - Must be authorized to witness statutory declarations in your jurisdiction]\n")
            f.write("[QUALIFICATION OF WITNESS, e.g., Justice of the Peace, Notary Public, etc.]\n")

        return template_path

    def _generate_apple_support_request_template(self, output_dir: str) -> str:
        """
        Generate Apple support request template

        Args:
            output_dir: Directory to save template

        Returns:
            str: Path to generated template
        """
        template_path = os.path.join(output_dir, "apple_support_request_template.txt")

        with open(template_path, "w") as f:
            f.write("APPLE SUPPORT REQUEST TEMPLATE\n")
            f.write("==============================\n\n")
            f.write("Subject: Inherited Device Access Request - Deceased Family Member\n\n")
            f.write("Dear Apple Support,\n\n")
            f.write("I am writing regarding an Apple device that I have inherited following the death of a family member. I am unable to access the device due to Activation Lock/Apple ID restrictions.\n\n")
            f.write("Device Details:\n")
            f.write("- Device Type: [iPhone/iPad/etc.]\n")
            f.write("- Model: [MODEL NUMBER]\n")
            f.write("- Serial Number: [SERIAL NUMBER]\n")
            f.write("- IMEI (if applicable): [IMEI NUMBER]\n\n")
            f.write("Deceased's Information:\n")
            f.write("- Name: [DECEASED'S FULL NAME]\n")
            f.write("- Date of Death: [DATE]\n")
            f.write("- Apple ID (if known): [APPLE ID EMAIL]\n\n")
            f.write("My Information:\n")
            f.write("- Name: [YOUR FULL NAME]\n")
            f.write("- Relationship to Deceased: [RELATIONSHIP]\n")
            f.write("- Contact Email: [YOUR EMAIL]\n")
            f.write("- Contact Phone: [YOUR PHONE]\n\n")
            f.write("I have prepared the following documentation to support my request:\n")
            f.write("1. Death Certificate\n")
            f.write("2. Proof of Inheritance (Will/Probate Document)\n")
            f.write("3. My Government-issued ID\n")
            f.write("4. Proof of Relationship to the Deceased\n")
            f.write("5. Proof of Purchase (if available)\n\n")
            f.write("I understand this is a sensitive matter that requires careful verification. I am prepared to provide any additional documentation or information that may be required to process this request.\n\n")
            f.write("Please advise on the next steps in this process and how I should submit the documentation securely.\n\n")
            f.write("Thank you for your assistance in this difficult time.\n\n")
            f.write("Sincerely,\n\n")
            f.write("[YOUR FULL NAME]\n")

        return template_path

    def _generate_documentation_checklist(self, output_dir: str) -> str:
        """
        Generate documentation checklist

        Args:
            output_dir: Directory to save checklist

        Returns:
            str: Path to generated checklist
        """
        checklist_path = os.path.join(output_dir, "documentation_checklist.txt")

        with open(checklist_path, "w") as f:
            f.write("DOCUMENTATION CHECKLIST FOR INHERITED DEVICE ACCESS\n")
            f.write("=================================================\n\n")
            f.write("Essential Documents:\n\n")
            f.write("[ ] 1. Death Certificate\n")
            f.write("    - Must be original or certified copy\n")
            f.write("    - Should clearly show the deceased's full name and date of death\n\n")
            f.write("[ ] 2. Proof of Inheritance\n")
            f.write("    - Will naming you as beneficiary, OR\n")
            f.write("    - Probate document, OR\n")
            f.write("    - Letter of Administration, OR\n")
            f.write("    - Court order establishing inheritance rights\n\n")
            f.write("[ ] 3. Your Government-issued ID\n")
            f.write("    - Passport, driver's license, or national ID card\n")
            f.write("    - Must be valid and not expired\n")
            f.write("    - Should clearly show your full name and photo\n\n")
            f.write("[ ] 4. Proof of Relationship to Deceased\n")
            f.write("    - Birth certificate (if child of deceased)\n")
            f.write("    - Marriage certificate (if spouse of deceased)\n")
            f.write("    - Other legal document establishing relationship\n\n")
            f.write("Additional Helpful Documents (if available):\n\n")
            f.write("[ ] 5. Proof of Purchase\n")
            f.write("    - Original receipt\n")
            f.write("    - Credit card statement showing purchase\n")
            f.write("    - Gift receipt\n\n")
            f.write("[ ] 6. Device Information\n")
            f.write("    - Serial number (check on back of device or in Settings)\n")
            f.write("    - IMEI number (for iPhones, dial *#06#)\n")
            f.write("    - Original packaging with device identifiers\n\n")
            f.write("[ ] 7. Completed Templates\n")
            f.write("    - Inheritance letter\n")
            f.write("    - Statutory declaration (witnessed/notarized)\n")
            f.write("    - Apple support request\n\n")
            f.write("Next Steps:\n\n")
            f.write("1. Gather all checked documents above\n")
            f.write("2. Contact Apple Support directly:\n")
            f.write("   - Visit: https://support.apple.com\n")
            f.write("   - Call: 1-800-MY-APPLE (US) or your country's Apple Support number\n")
            f.write("   - Visit an Apple Store with an appointment\n")
            f.write("3. Explain the situation and be prepared to submit documentation\n")
            f.write("4. Follow Apple's specific instructions for your case\n\n")
            f.write("Note: Apple reviews each case individually. The process may take time and additional documentation may be requested.\n")

        return checklist_path

    def provide_apple_support_contact_info(self) -> Dict[str, str]:
        """
        Provide Apple support contact information

        Returns:
            Dict[str, str]: Dictionary of contact information
        """
        self.log("Providing Apple support contact information")

        contact_info = {
            "website": "https://support.apple.com",
            "phone_us": "1-800-MY-APPLE (1-800-692-7753)",
            "inheritance_info": "https://support.apple.com/en-us/HT208510",
            "apple_store": "https://www.apple.com/retail/",
            "online_chat": "https://getsupport.apple.com/"
        }

        self.log("Apple Support Website: " + contact_info["website"])
        self.log("Apple Support Phone (US): " + contact_info["phone_us"])
        self.log("Apple Support Article on Inheritance: " + contact_info["inheritance_info"])

        return contact_info

    def generate_limited_documentation_templates(self, output_dir: str = None) -> Dict[str, str]:
        """
        Generate templates for cases with limited documentation

        This method creates templates for users who cannot provide all standard
        documentation but have limited proof like affidavits.

        Args:
            output_dir: Directory to save templates (optional)

        Returns:
            Dict[str, str]: Dictionary of template paths
        """
        self.log("Generating templates for limited documentation cases")

        # Create temporary directory if output_dir not provided
        if output_dir is None:
            output_dir = tempfile.mkdtemp(prefix="limited_docs_")
            self.log(f"Created temporary directory: {output_dir}")
        else:
            os.makedirs(output_dir, exist_ok=True)
            self.log(f"Using directory: {output_dir}")

        # Define templates
        templates = {
            "affidavit_template": self._generate_affidavit_template(output_dir),
            "third_party_verification": self._generate_third_party_verification(output_dir),
            "circumstantial_evidence": self._generate_circumstantial_evidence_guide(output_dir),
            "legal_aid_resources": self._generate_legal_aid_resources(output_dir),
            "alternative_options": self._generate_alternative_options_guide(output_dir)
        }

        self.log(f"Generated {len(templates)} templates for limited documentation cases")
        for name, path in templates.items():
            self.log(f"- {name}: {path}")

        return templates

    def _generate_affidavit_template(self, output_dir: str) -> str:
        """
        Generate affidavit template for limited documentation cases

        Args:
            output_dir: Directory to save template

        Returns:
            str: Path to generated template
        """
        template_path = os.path.join(output_dir, "affidavit_template.txt")

        with open(template_path, "w") as f:
            f.write("AFFIDAVIT OF OWNERSHIP AND CIRCUMSTANCES\n")
            f.write("========================================\n\n")
            f.write("STATE/PROVINCE OF [YOUR STATE/PROVINCE]\n")
            f.write("COUNTY/REGION OF [YOUR COUNTY/REGION]\n\n")
            f.write("I, [YOUR FULL NAME], being duly sworn, hereby state:\n\n")
            f.write("1. I am over eighteen years of age and competent to make this affidavit.\n\n")
            f.write("2. I am the rightful owner of an Apple [DEVICE TYPE], Model [MODEL NUMBER], with Serial Number [SERIAL NUMBER if known] and/or IMEI [IMEI NUMBER if known].\n\n")
            f.write("3. I acquired this device from [PREVIOUS OWNER'S NAME] who is now deceased.\n\n")
            f.write("4. My relationship to the deceased was [RELATIONSHIP, e.g., son, daughter, spouse, friend].\n\n")
            f.write("5. I am unable to provide standard documentation for the following reason(s):\n")
            f.write("   [EXPLAIN IN DETAIL why standard documentation is unavailable. For example:]\n")
            f.write("   - The deceased passed away without a formal will\n")
            f.write("   - The death occurred in circumstances where documentation is difficult to obtain\n")
            f.write("   - The device was gifted to me verbally before death\n")
            f.write("   - Other relevant circumstances\n\n")
            f.write("6. I can provide the following evidence of my legitimate ownership:\n")
            f.write("   [LIST ALL EVIDENCE YOU CAN PROVIDE, such as:]\n")
            f.write("   - Photographs of the deceased using the device\n")
            f.write("   - Text messages or emails referring to the device being given to you\n")
            f.write("   - Statements from other family members confirming your ownership\n")
            f.write("   - Partial payment records or gift receipts\n")
            f.write("   - Any other relevant evidence\n\n")
            f.write("7. I understand that making false statements in this affidavit may subject me to legal penalties for perjury.\n\n")
            f.write("8. I am making this affidavit to support my request to Apple Inc. to assist me in accessing this device.\n\n")
            f.write("FURTHER AFFIANT SAYETH NOT.\n\n")
            f.write("_______________________\n")
            f.write("[YOUR FULL NAME]\n\n")
            f.write("Sworn to and subscribed before me this ____ day of ____________, 20___.\n\n")
            f.write("_______________________\n")
            f.write("Notary Public\n")
            f.write("My Commission Expires: ____________\n\n")
            f.write("NOTARY SEAL\n\n")
            f.write("NOTE: This affidavit should be notarized by a licensed notary public in your jurisdiction.")

        return template_path

    def _generate_third_party_verification(self, output_dir: str) -> str:
        """
        Generate third-party verification template

        Args:
            output_dir: Directory to save template

        Returns:
            str: Path to generated template
        """
        template_path = os.path.join(output_dir, "third_party_verification.txt")

        with open(template_path, "w") as f:
            f.write("THIRD-PARTY VERIFICATION OF OWNERSHIP\n")
            f.write("===================================\n\n")
            f.write("I, [THIRD PARTY FULL NAME], hereby verify the following:\n\n")
            f.write("1. I am over eighteen years of age and personally know [DEVICE OWNER'S NAME].\n\n")
            f.write("2. My relationship to [DEVICE OWNER'S NAME] is [RELATIONSHIP, e.g., family friend, colleague, neighbor].\n\n")
            f.write("3. I also knew [DECEASED'S NAME] before their passing.\n\n")
            f.write("4. I have personal knowledge that the Apple [DEVICE TYPE] with [ANY IDENTIFYING FEATURES] belonged to [DECEASED'S NAME] and was intended to be given to/inherited by [DEVICE OWNER'S NAME].\n\n")
            f.write("5. The basis of my knowledge is:\n")
            f.write("   [EXPLAIN HOW YOU KNOW THIS INFORMATION, for example:]\n")
            f.write("   - I was present when the device was purchased\n")
            f.write("   - I witnessed the deceased using the device regularly\n")
            f.write("   - I heard the deceased state their intention to give the device to the current owner\n")
            f.write("   - I helped transfer the deceased's belongings after their passing\n")
            f.write("   - Other relevant information\n\n")
            f.write("6. I make this verification to support [DEVICE OWNER'S NAME]'s legitimate claim to the device.\n\n")
            f.write("7. I understand that making false statements in this verification may have legal consequences.\n\n")
            f.write("Date: ________________\n\n")
            f.write("_______________________\n")
            f.write("[THIRD PARTY FULL NAME]\n\n")
            f.write("Contact Information:\n")
            f.write("Phone: ________________\n")
            f.write("Email: ________________\n")
            f.write("Address: ________________\n\n")
            f.write("NOTE: For stronger verification, this document can be notarized.")

        return template_path

    def _generate_circumstantial_evidence_guide(self, output_dir: str) -> str:
        """
        Generate guide for gathering circumstantial evidence

        Args:
            output_dir: Directory to save guide

        Returns:
            str: Path to generated guide
        """
        guide_path = os.path.join(output_dir, "circumstantial_evidence_guide.txt")

        with open(guide_path, "w") as f:
            f.write("GUIDE TO GATHERING CIRCUMSTANTIAL EVIDENCE\n")
            f.write("========================================\n\n")
            f.write("When standard documentation is unavailable, gathering strong circumstantial evidence can help support your claim. This guide will help you collect and organize evidence that may assist in your case.\n\n")
            f.write("1. PHOTOGRAPHS AND VIDEOS\n")
            f.write("   - Photos/videos of the deceased using the device\n")
            f.write("   - Photos of the device in the deceased's home\n")
            f.write("   - Photos showing distinctive features of the device (case, scratches, stickers)\n")
            f.write("   - Screenshots of the device backed up to your computer (if available)\n\n")
            f.write("2. DIGITAL EVIDENCE\n")
            f.write("   - Email receipts from when the device was purchased\n")
            f.write("   - Text messages or emails mentioning the device\n")
            f.write("   - Social media posts showing or mentioning the device\n")
            f.write("   - Cloud backups that might contain device information\n")
            f.write("   - Shared photo albums that include photos taken with the device\n\n")
            f.write("3. FINANCIAL RECORDS\n")
            f.write("   - Bank or credit card statements showing the purchase\n")
            f.write("   - Insurance documents listing the device\n")
            f.write("   - Warranty registration information\n")
            f.write("   - Service or repair receipts\n\n")
            f.write("4. WITNESS STATEMENTS\n")
            f.write("   - Statements from family members\n")
            f.write("   - Statements from friends who knew about the device\n")
            f.write("   - Statements from colleagues if it was used for work\n\n")
            f.write("5. KNOWLEDGE OF THE DEVICE\n")
            f.write("   - List of apps that were installed\n")
            f.write("   - Description of the wallpaper/background\n")
            f.write("   - Names of contacts in the address book\n")
            f.write("   - Description of photos or content on the device\n\n")
            f.write("6. ORGANIZING YOUR EVIDENCE\n")
            f.write("   - Create a timeline of the device's history\n")
            f.write("   - Organize all evidence by type\n")
            f.write("   - Make copies of all evidence\n")
            f.write("   - Create a summary document explaining each piece of evidence\n\n")
            f.write("Remember: The more evidence you can provide, the stronger your case will be. Even small details can help establish the legitimacy of your claim.")

        return guide_path

    def _generate_legal_aid_resources(self, output_dir: str) -> str:
        """
        Generate guide for legal aid resources

        Args:
            output_dir: Directory to save guide

        Returns:
            str: Path to generated guide
        """
        guide_path = os.path.join(output_dir, "legal_aid_resources.txt")

        with open(guide_path, "w") as f:
            f.write("LEGAL AID RESOURCES\n")
            f.write("===================\n\n")
            f.write("If you're struggling with the inheritance process and need legal assistance, the following resources may help:\n\n")
            f.write("1. LEGAL AID ORGANIZATIONS\n")
            f.write("   - Legal Services Corporation: https://www.lsc.gov/about-lsc/what-legal-aid/get-legal-help\n")
            f.write("   - American Bar Association Free Legal Answers: https://abafreelegalanswers.org/\n")
            f.write("   - LawHelp.org: https://www.lawhelp.org/\n\n")
            f.write("2. PRO BONO LEGAL SERVICES\n")
            f.write("   - Many law firms offer pro bono (free) services for certain cases\n")
            f.write("   - Contact your state or local bar association for referrals\n")
            f.write("   - Law school legal clinics often provide free legal assistance\n\n")
            f.write("3. CONSUMER ADVOCACY GROUPS\n")
            f.write("   - Electronic Frontier Foundation: https://www.eff.org/\n")
            f.write("   - Consumer Reports: https://www.consumerreports.org/\n")
            f.write("   - Consumer Financial Protection Bureau: https://www.consumerfinance.gov/\n\n")
            f.write("4. ONLINE LEGAL RESOURCES\n")
            f.write("   - Nolo: https://www.nolo.com/ (free legal information)\n")
            f.write("   - FindLaw: https://www.findlaw.com/ (legal information and lawyer directory)\n")
            f.write("   - Avvo: https://www.avvo.com/ (legal Q&A and lawyer directory)\n\n")
            f.write("5. ESTATE PLANNING ASSISTANCE\n")
            f.write("   - AARP: https://www.aarp.org/money/investing/info-2016/free-legal-advice-low-income.html\n")
            f.write("   - National Academy of Elder Law Attorneys: https://www.naela.org/\n\n")
            f.write("6. MEDIATION SERVICES\n")
            f.write("   - Community mediation centers often offer low-cost services\n")
            f.write("   - Court-connected mediation programs\n")
            f.write("   - Online mediation services\n\n")
            f.write("Remember: Many legal aid services have income eligibility requirements. Be prepared to provide information about your financial situation when seeking assistance.")

        return guide_path

    def _generate_alternative_options_guide(self, output_dir: str) -> str:
        """
        Generate guide for alternative options when recovery isn't possible

        Args:
            output_dir: Directory to save guide

        Returns:
            str: Path to generated guide
        """
        guide_path = os.path.join(output_dir, "alternative_options_guide.txt")

        with open(guide_path, "w") as f:
            f.write("ALTERNATIVE OPTIONS WHEN RECOVERY ISN'T POSSIBLE\n")
            f.write("=============================================\n\n")
            f.write("If you've exhausted all options for accessing the device through Apple's official channels, consider these alternatives before disposing of the device:\n\n")
            f.write("1. DEVICE REPURPOSING OPTIONS\n")
            f.write("   - Trade-in programs: Some retailers offer trade-in credit even for locked devices\n")
            f.write("   - Sell for parts: The device may have value for its components\n")
            f.write("   - Donation for education: Some educational programs accept locked devices for teaching purposes\n")
            f.write("   - Recycling programs: Ensure proper disposal and recycling of electronic components\n\n")
            f.write("2. DATA RECOVERY ALTERNATIVES\n")
            f.write("   - Check if the deceased used iCloud backups (accessible with their Apple ID)\n")
            f.write("   - Look for iTunes/Finder backups on their computer\n")
            f.write("   - Check if photos were synced to Google Photos or similar services\n")
            f.write("   - Contact mobile carrier for possible cloud backups\n\n")
            f.write("3. PROFESSIONAL SERVICES\n")
            f.write("   - Data recovery specialists (though success with locked iPhones is limited)\n")
            f.write("   - Apple Authorized Service Providers may offer additional options\n")
            f.write("   - Legal services specializing in digital asset recovery\n\n")
            f.write("4. DOCUMENTATION FOR INSURANCE OR TAX PURPOSES\n")
            f.write("   - Document the device and situation for insurance claims\n")
            f.write("   - Keep records for potential tax deductions (donations/losses)\n")
            f.write("   - Maintain evidence of ownership for estate purposes\n\n")
            f.write("5. FUTURE PLANNING\n")
            f.write("   - Set up Digital Legacy contacts for your own Apple ID\n")
            f.write("   - Create a digital estate plan for your own devices\n")
            f.write("   - Document your devices and access information for heirs\n\n")
            f.write("Remember: Even if you cannot access the device, it may still have value or purpose. Consider all options before disposal.")

        return guide_path

    def provide_limited_documentation_guidance(self) -> InheritanceSupportResult:
        """
        Provide guidance for cases with limited documentation

        Returns:
            InheritanceSupportResult: The result of the guidance
        """
        self.log("Starting guidance for limited documentation cases")

        # Provide general guidance
        self.log("\nFor inherited devices with limited documentation:")
        self.log("1. Apple's standard process typically requires formal documentation")
        self.log("2. When standard documentation is unavailable, alternative evidence may help")
        self.log("3. Building a strong case with multiple forms of evidence is important")
        self.log("4. Legal assistance may be beneficial in complex cases")
        self.log("5. Be prepared with a clear explanation of your circumstances")

        # Return guidance result
        return InheritanceSupportResult.LIMITED_DOCUMENTATION_SUPPORT

# Example usage
if __name__ == "__main__":
    # Create inheritance support
    support = InheritanceSupport(debug=True)

    # Provide guidance
    support.provide_inheritance_guidance()

    # Generate documentation templates
    templates = support.generate_documentation_templates()

    # Provide contact information
    contact_info = support.provide_apple_support_contact_info()

    # Print logs
    print("\nInheritance Support Logs:")
    for log in support.logs:
        print(log)
