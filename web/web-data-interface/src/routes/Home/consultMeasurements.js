export const consultMeasurements = (mockData, userId, startDate, endDate, filterType, inHouseFilter) => {

  let userMeasurements = mockData.filter(
    (measurement) => measurement.userid === userId
  );

  if (startDate) {
    userMeasurements = userMeasurements.filter((measurement) => {
      const measurementDate = new formatDate(measurement.datetime).toISOString().split("T")[0];
      return measurementDate >= startDate;
    });
  }

  if (endDate) {
    userMeasurements = userMeasurements.filter((measurement) => {
      const measurementDate = new formatDate(measurement.datetime).toISOString().split("T")[0];
      return measurementDate <= endDate;
    });
  }

  if (filterType) {
    userMeasurements = userMeasurements.filter(
      (measurement) => measurement.type.toString() === filterType
    );
  }

  if (inHouseFilter !== "") {
    const inHouseValue = inHouseFilter === "true";
    userMeasurements = userMeasurements.filter(
      (measurement) => measurement.inhouse === inHouseValue
    );
  }

  return userMeasurements;
};
