tests ={       
    "EDSNBusinessDocumentHeader/ConversationID" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"],
        "Duplicate_Element":["duplicate_element"]
    },
    "EDSNBusinessDocumentHeader/CorrelationID" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "EDSNBusinessDocumentHeader/CreationTimestamp" :{
        "Correct_Value":["2021-03-01T22:00:00Z","2021-01-02T22:00:00Z","2021-01-03T22:00:00Z","2021-01-04T22:00:00Z"],
        "Invalid_Value":["2021-01-35T22:00:00Z","2021-15-02T22:00:00Z","2021-01-02T00 :00:80Z","2021-01-02T00:00:62Z","2021-01-02T00:62:00Z","2021-01-02T27:00:00Z"],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "EDSNBusinessDocumentHeader/DocumentID" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "EDSNBusinessDocumentHeader/ExpiresAt" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "EDSNBusinessDocumentHeader/MessageID" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "EDSNBusinessDocumentHeader/ProcessTypeID" :{
        "Correct_Value":["N10","N20"],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "EDSNBusinessDocumentHeader/RepeatedRequest" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "EDSNBusinessDocumentHeader/TestRequest" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "EDSNBusinessDocumentHeader/Destination/Receiver/Authority" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "EDSNBusinessDocumentHeader/Destination/Receiver/ContactTypeIdentifier" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "EDSNBusinessDocumentHeader/Destination/Receiver/ReceiverID" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "EDSNBusinessDocumentHeader/Destination/Service/ServiceMethod" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "EDSNBusinessDocumentHeader/Destination/Service/ServiceName" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "EDSNBusinessDocumentHeader/Manifest/NumberofItems" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "EDSNBusinessDocumentHeader/Manifest/ManifestItem/Description" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "EDSNBusinessDocumentHeader/Manifest/ManifestItem/LanguageCode" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "EDSNBusinessDocumentHeader/Manifest/ManifestItem/MimeTypeQualifierCode" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "EDSNBusinessDocumentHeader/Manifest/ManifestItem/UniformResourceIdentifier" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "EDSNBusinessDocumentHeader/Source/Authority" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "EDSNBusinessDocumentHeader/Source/ContactTypeIdentifier" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "EDSNBusinessDocumentHeader/Source/SenderID" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Acknowledgement_MarketDocument/mRID" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Acknowledgement_MarketDocument/createdDateTime" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Acknowledgement_MarketDocument/Received_MarketDocument/mRID" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Acknowledgement_MarketDocument/Reason/code" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Acknowledgement_MarketDocument/Reason/text" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Measurement_Series/mRID" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Measurement_Series/referenceTimeSeries_mRID" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Measurement_Series/reasonRevisionRequest" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Measurement_Series/explanationRevisionRequest" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Measurement_Series/MarketEvaluationPoint/mRID" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Measurement_Series/MarketParticipant/mRID" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Measurement_Series/MarketParticipant/MarketRole/type" :{
        "Correct_Value":["MDR"],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Measurement_Series/DateAndOrTime/startDateTime" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Measurement_Series/DateAndOrTime/endDateTime" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Measurement_Series/Detail_Series/resolution" :{
        "Correct_Value":["PT5M","PT15M","PT60M"],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Measurement_Series/Detail_Series/Product/identification" :{
        "Correct_Value":["8716867000030","8716867000047","5410000100016(gas)"],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Measurement_Series/Detail_Series/Product/measureUnit" :{
        "Correct_Value":["KWH","K3","NM3"],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Measurement_Series/Detail_Series/FlowDirection/direction" :{
        "Correct_Value":["E17","E18"],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Measurement_Series/Detail_Series/Original_Point/position" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Measurement_Series/Detail_Series/Original_Point/quantity" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Measurement_Series/Detail_Series/Proposed_Point/position" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Measurement_Series/Detail_Series/Proposed_Point/quantity" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Measurement_Series/referenceRevisionRequest_mRID" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Measurement_Series/Domain/mRID" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Measurement_Series/Domain/sourceDomain" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Measurement_Series/Domain/sinkDomain" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Measurement_Series/Detail_Series/Point/position" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Measurement_Series/Detail_Series/Point/quantity" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Measurement_Series/Detail_Series/Point/origin" :{
        "Correct_Value":["MSR","UMS","CLC","MSR"],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Measurement_Series/Detail_Series/Point/validationStatus" :{
        "Correct_Value":["VLD","NVL","MNL"],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Measurement_Series/Detail_Series/Point/repairMethod" :{
        "Correct_Value":["MT","CFF","CIN","IMC","NCD","CMR","ENF","RBR","RGR","GMR"],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Measurement_Series/RestVolume_Quantity/quantity" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Measurement_Series/referenceAllocation_mRID" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Measurement_Series/product" :{
        "Correct_Value":["023"],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Volume_Series/mRID" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Volume_Series/referenceRevisionRequest_mRID" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Volume_Series/MarketEvaluationPoint/mRID" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Volume_Series/MarketParticipant/mRID" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Volume_Series/Domain/mRID" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Volume_Series/DateAndOrTime/startDateTime" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Volume_Series/DateAndOrTime/endDateTime" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Volume_Series/Volume_Quantity/quantity" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Volume_Series/Volume_Quantity/timeframeType" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Volume_Series/RestVolume_Quantity/quantity" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Volume_Series/Max_Quantity/quantity" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Volume_Series/WeekMax_Quantity/quantity" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Volume_Series/Register/mRID" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Volume_Series/Register/timeframeType" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Volume_Series/Register/Product/identification" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Volume_Series/Register/Product/measureUnit" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Volume_Series/Register/FlowDirection/direction" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Volume_Series/Register/Meter/mRID" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Volume_Series/Register/Reading/value" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    },
    "Volume_Series/Register/Reading/origin" :{
        "Correct_Value":[""],
        "Invalid_Value":[""],
        "Empty_Value":[""],
        "Missing_Element":["delete_element"]
    }
}