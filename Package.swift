// swift-tools-version:5.3
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
    name: "force-pusher",
    dependencies: [
        .package(name: "OctoKit", url: "https://github.com/nerdishbynature/octokit.swift", from: "0.9.0"),
        .package(name: "swift-commands", url: "https://github.com/QiuZhiFei/swift-commands", from: "0.3.0"),
    ],
    targets: [
        .target(
            name: "ForcePusher",
            dependencies: [
                "OctoKit",
                .product(name: "Commands", package: "swift-commands")
            ]),
    ]
)
